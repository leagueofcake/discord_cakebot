import asyncio
import sys
import requests
import sqlite3

from discord import errors as discord_errors

import cakebot_help
from datetime import datetime
import cakebot_config
from modules.helpers import is_integer, get_full_username
from modules.misc import return_troll, parse_duration_str
from modules.permissions import get_permissions, set_permissions, update_permissions, allowed_perm_commands
from modules.music import get_music_prefix, add_music_prefix, update_music_prefix, find_song_by_name, \
    find_album, find_song_by_id, search_songs, make_song_results, Song
from modules.modtools import add_log_channel, update_log_channel, get_log_channel_id, gen_edit_message_log, \
    gen_delete_message_log, purge_messages


class Bot:
    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect(cakebot_config.DB_PATH)
        self.c = self.conn.cursor()

    async def temp_message(self, channel, message, time=5):
        tmp = await self.say(channel, message)
        await asyncio.sleep(time)
        await self.delete(tmp)

    async def delete(self, message):
        await self.client.delete_message(message)

    async def say(self, channel, message):
        return await self.client.send_message(channel, message)

    async def hello(self, message):
        await self.say(message.channel, 'Hello {}!'.format(message.author.mention))

    async def bye(self, message):
        if self._is_owner(message.author):
            await self.say(message.channel, 'Logging out, bye!')
            sys.exit()
        else:
            await self.say(message.channel, 'I\'m not going anywhere!')

    def auth_function(self, f):
        async def ret_fun(message, owner_auth=False, manage_server_auth=False, require_non_cakebot=False, cakebot_perm=None):
            owner_check = owner_auth and self._is_owner(message.author)
            manage_server_check = manage_server_auth and self._can_manage_server(message.author, message.channel)
            is_cakebot_check = (not require_non_cakebot) or (require_non_cakebot and not self._is_cakebot(message.author))
            no_auth = not owner_auth and not manage_server_auth and not cakebot_perm

            perms = get_permissions(self.c, message.author.id, message.server.id)
            cakebot_perm_check = cakebot_perm and perms and cakebot_perm in perms

            if is_cakebot_check and (no_auth or owner_check or manage_server_check or cakebot_perm_check):
                await f(message)
            else:
                await self.say(message.channel, 'You\'re not allowed to do that!')
        return ret_fun

    async def say_in_room(self, message):
        async def inner(m):
            if m.channel_mentions:
                await self.say(m.channel_mentions[0], ' '.join(m.content.split()[2:]))
            else:
                await self.say(m.channel, 'No room specified!')
            await self.delete(m)

        await self.auth_function(inner)(message, owner_auth=True)

    async def _print_permissions(self, message, user):
        perms = get_permissions(self.c, user.id, message.server.id)
        if perms:
            perm_message = 'Permissions for {}: {}'.format(user, perms)
        else:
            perm_message = 'There are no set permissions for: {}'.format(user)
        if self._can_manage_server(user, message.channel):
            perm_message += '\nThis user has manage_server permissions.'

        await self.say(message.channel, perm_message)

    async def _set_permissions(self, message, user):
        async def inner(m):
            perms = get_permissions(self.c, user.id, m.server.id)
            add_perms = [comm for comm in m.content.split()[2:] if comm in allowed_perm_commands]  # Filter allowed permission commands

            if add_perms:
                if perms:
                    current_perms = perms[0]
                    new_perms = current_perms + ',' + ','.join(add_perms)
                    update_permissions(self.c, user.id, m.server.id, new_perms)
                else:
                    set_permissions(self.c, user.id, m.server.id, add_perms)
                self.conn.commit()
                add_message = 'Added permissions: `{}` to {}'.format(','.join(add_perms), user)
                await self.say(m.channel, add_message)
            else:
                await self.say(m.channel, 'No permissions were added to {}!'.format(user))
        await self.auth_function(inner)(message, require_non_cakebot=True, manage_server_auth=True, owner_auth=True)

    async def permissions(self, message):
        args = message.content.split()

        # Gets permissions for mentioned user if given, otherwise defaults to calling user
        user = message.author
        if message.mentions:
            user = message.mentions[0]  # Find id of first mentioned user

        if len(args) == 1 or len(args) == 2:
            await self._print_permissions(message, user)
        elif len(args) > 2:
            await self._set_permissions(message, user)

    async def timed_cats(self, message):
        async def inner(m):
            times, duration_str = parse_duration_str(m.content.split())
            unit_time = cakebot_config.time_map[duration_str][0]

            unit = cakebot_config.time_map[duration_str][1]
            unit_plural = cakebot_config.time_map[duration_str][2]

            if times == 1:
                unit_plural = unit

            await self.say(m.channel, 'Sending cats every {} for {} {}!'.format(unit, times, unit_plural))

            for i in range(times):
                cat_url = requests.get('http://random.cat/meow').json()['file']
                await self.say(m.channel, cat_url)
                if i == times - 1:
                    await self.say(m.channel, 'Finished sending cats!')
                    break
                await asyncio.sleep(unit_time)
        await self.auth_function(inner)(message, owner_auth=True)

    async def troll_url(self, message):
        await self.say(message.channel, return_troll(message.content.split()[1]))
        await self.delete(message)

    async def redirect(self, message):
        room = message.channel_mentions[0]
        await self.say(room, '`{}` redirected:'.format(message.author))
        await self.say(room, ' '.join(message.content.split()[2:]))
        await self.delete(message)

    async def purge(self, message):
        async def inner(m):
            args = m.content.split()

            await self.delete(m)
            if len(args) < 2:
                await self.say(m.channel, "Please specify the number of messages to purge.")
            else:
                if m.mentions and len(args) >= 3:
                    purge_user = m.mentions[0]  # Find id of first mentioned user
                    if not is_integer(args[2]):
                        await self.say(m.channel, "Please specify a valid number of messages to purge. (1-100)")
                    else:
                        num = int(args[2])
                        await purge_messages(message=message, client=self.client, purge_user=purge_user, num=num)
                else:
                    if not is_integer(args[1]):
                        await self.say(m.channel, "Please specify a valid number of messages to purge. (1-100)")
                    else:
                        num = int(args[1])
                        try:
                            deleted = await self.client.purge_from(m.channel, limit=num)
                            await self.temp_message(m.channel, "Purged {} messages.".format(len(deleted)))
                        except discord_errors.HTTPException:  # Delete individually
                            async for log in self.client.logs_from(m.channel, limit=num):
                                await self.delete(log)

        await self.auth_function(inner)(message, manage_server_auth=True, require_non_cakebot=True)

    async def del_user_messages(self, message):
        async def inner(m):
            args = m.content.split()
            if len(args) == 1 or (len(args) == 2 and is_integer(args[1]) and args[1] == '1'):
                await self.delete(m)
                async for log in self.client.logs_from(m.channel, limit=500):
                    if log.author.id == m.author.id:
                        await self.delete(log)
                        break
            elif len(args) == 2:
                await self.delete(m)
                purge_user_id = m.author
                if not is_integer(args[1]):
                    await self.say(m.channel, "Please specify a valid number of messages to delete. (1-100)")
                else:
                    num = int(args[1])
                    await purge_messages(message=m, client=self.client, purge_user=purge_user_id, num=num)
        await self.auth_function(inner)(message, require_non_cakebot=True)

    async def _print_log_channel(self, message):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, message.server.id))
        if log_channel:
            await self.temp_message(message.channel, 'Log channel is: {}'.format(log_channel.mention))
        else:
            await self.temp_message(message.channel, 'No log channel configured! Add one with `!logchannel set`')

    async def _set_log_channel(self, message):
        async def inner(m):
            log_channel = self.client.get_channel(get_log_channel_id(self.c, m.server.id))
            if log_channel:
                update_log_channel(self.c, m.server.id, m.channel.id)
            else:
                add_log_channel(self.c, m.server.id, m.channel.id)
            await self.say(m.channel, 'Set {} as the log channel!'.format(m.channel.mention))
            self.conn.commit()
        await self.auth_function(inner)(message, manage_server_auth=True, cakebot_perm='logchannel', require_non_cakebot=True)

    async def log_channel(self, message):
        args = message.content.split()
        if len(args) == 1:
            await self._print_log_channel(message)
        else:
            if len(args) == 2 and args[1] == 'set':
                await self._set_log_channel(message)

    async def help(self, message):
        args = message.content.split()
        if len(args) > 1:  # specific command
            command = args[1]
            try:
                await self.temp_message(message.channel, cakebot_help.get_entry(command), time=10)
            except KeyError:
                await self.temp_message(message.channel, 'Command not found! do ``!help`` for the command list.', time=10)
        else:  # command list summary
            await self.temp_message(message.channel, cakebot_help.generate_summary(), time=10)

    async def _print_music_prefix(self, message):
        music_prefix = get_music_prefix(self.c, message.server.id)
        if music_prefix:
            await self.temp_message(message.channel, 'Current music prefix for this server is: `{}`'.format(music_prefix))
        else:
            await self.temp_message(message.channel, 'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')

    async def _set_music_prefix(self, message):
        async def inner(m):
            music_prefix = get_music_prefix(self.c, m.server.id)
            new_prefix = ' '.join(m.content.split()[1:])
            if music_prefix:
                update_music_prefix(self.c, m.server.id, new_prefix)
                await self.say(m.channel, 'Updated music prefix for this server to: `{}`'.format(new_prefix))
            else:
                add_music_prefix(self.c, m.server.id, new_prefix)
                await self.say(m.channel, 'Set music prefix for this server to: `{}`'.format(new_prefix))
            self.conn.commit()
        await self.auth_function(inner)(message, manage_server_auth=True, cakebot_perm='musicprefix', require_non_cakebot=True)

    async def music_prefix(self, message):
        args = message.content.split()
        if len(args) == 1:
            await self._print_music_prefix(message)
        else:
            await self._set_music_prefix(message)

    async def queue_songs(self, message, music_prefix, songs):
        if music_prefix:
            for song in songs:
                song = Song(*song)

                if music_prefix:
                    await self.temp_message(message.channel, '{} {}'.format(music_prefix, song.link), time=3)
                    await self.say(message.channel, '{} queued: {}'.format(message.author, song.name))
        else:
            await self.temp_message(message.channel, 'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')

    async def search_and_play(self, message):
        args = message.content.split()
        command = args[0]
        prefix = get_music_prefix(self.c, message.server.id)
        if command == '!play' or command == '!search':
            search = '%{}%'.format(' '.join(args[1:]).lower())
            if command == '!play':
                found = find_song_by_name(self.c, search)
            elif command == '!search':
                found = search_songs(self.c, search)

            if len(found) == 1 and command == '!play':
                await self.queue_songs(message, prefix, found)
            elif len(found) > 1 or command == '!search':
                tmp = await self.say(message.channel, make_song_results(found))

                def check(msg):
                    splitted = msg.content.split()
                    return len(splitted) >= 2 and splitted[0] == '!page' and is_integer(splitted[1])

                msg = await self.client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                while msg is not None:
                    await self.delete(msg)
                    await self.delete(tmp)

                    page_num = msg.content.split()[1]
                    tmp = await self.say(message.channel, make_song_results(found, (int(page_num) - 1) * 13))
                    msg = await self.client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                await asyncio.sleep(cakebot_config.MUSIC_SEARCH_RESULT_TIME)
                await self.delete(tmp)
        else:
            found = None
            if command == '!playalbum':
                found = find_album(self.c, ' '.join(args[1:]))
                await self.say(message.channel, "Queueing the following songs. Confirm with ``!yes`` or refine your search terms.")

                def check(msg):
                    splitted = msg.content.split()
                    return msg.content == '!yes' or (len(splitted) >= 2 and splitted[0] == '!page' and is_integer(splitted[1]))

                tmp = await self.say(message.channel, make_song_results(found))
                msg = await self.client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                while msg is not None:
                    await self.delete(msg)
                    await self.delete(tmp)

                    if msg.content == '!yes':
                        await self.queue_songs(message, prefix, found)
                        break

                    page_num = msg.content.split()[1]
                    tmp = await self.say(message.channel, make_song_results(found, (int(page_num) - 1) * 13))
                    msg = await self.client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                await asyncio.sleep(cakebot_config.MUSIC_SEARCH_RESULT_TIME)
                await self.delete(tmp)
            elif command == '!playid':
                found = find_song_by_id(self.c, args[1])
                await self.queue_songs(message, prefix, found)

        if not found:
            await self.say(message.channel, "Couldn't find any matching songs!")

    async def handle_channel_update(self, before, after):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, before.server.id))

        if log_channel:
            local_message_time = datetime.now().strftime("%H:%M:%S")

            channel_mention = before.mention
            if before.name != after.name:
                message = '[{}] {} *changed channel name*\n' \
                          'Before: {}\n' \
                          'After+: {}'.format(local_message_time, channel_mention, before.name, after.name)
                await self.say(log_channel, message)
            if before.topic != after.topic:
                message = '[{}] {} *changed topic contents*\n' \
                          'Before: {}\n' \
                          'After+: {}'.format(local_message_time, channel_mention, before.topic, after.topic)
                await self.say(log_channel, message)

    async def handle_edited_message(self, before, after):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, before.server.id))
        if log_channel and before.content != after.content:
            await self.say(log_channel, gen_edit_message_log(before, after))

    async def handle_deleted_message(self, message):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, message.server.id))

        if log_channel:
            await self.say(log_channel, gen_delete_message_log(message))

    async def handle_member_update(self, before, after):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, before.server.id))

        if log_channel:
            local_message_time = datetime.now().strftime("%H:%M:%S")
            before_roles = ", ".join([role.name for role in before.roles if role.name != "@everyone"])
            after_roles = ", ".join([role.name for role in after.roles if role.name != "@everyone"])

            if before.nick != after.nick:
                message = '[{}] {} *changed nickname*\n' \
                          'Before: {}\n' \
                          'After+: {}'.format(local_message_time, get_full_username(before),
                                              before.display_name,
                                              after.display_name)
                await self.say(log_channel, message)

            elif before_roles != after_roles:
                message = '[{}] {} *changed roles*\n' \
                          'Before: {}\n' \
                          'After+: {}'.format(local_message_time, get_full_username(before),
                                              before_roles,
                                              after_roles)
                await self.say(log_channel, message)

        if before.game != after.game:
            await self._auto_rename_voice_channel(before, after)

    async def _auto_rename_voice_channel(self, before, after):
        if before.server.id in ("139345703800406016", "178312027041824768"):  # Only use on main/dev server
            default_list = ["Gaming Channel 1", "Gaming Channel 2", "Gaming Channel 3", "Music Channel"]

            if after.voice_channel:
                game_count = {}
                voice_members = after.voice_channel.voice_members

                for member in voice_members:
                    if member.game:
                        if member.game.name not in game_count:
                            game_count[member.game.name] = 1
                        else:
                            game_count[member.game.name] += 1
                if game_count:
                    # Select game with highest current players
                    new_channel_names = [key for m in [max(game_count.values())] for key,val in game_count.items() if val == m]
                    for new_channel_name in new_channel_names:
                        if new_channel_name:  # Non-blank new channel name, set as new channel name
                            await self.client.edit_channel(after.voice_channel, name=new_channel_name)
                            break
                else:
                    default_name = default_list[after.voice_channel.position]
                    await self.client.edit_channel(after.voice_channel, name=default_name)

                if before.voice_channel:
                    if len(before.voice_channel.voice_members) == 0:  # No more members, reset to default name
                        default_name = default_list[before.voice_channel.position]
                        await self.client.edit_channel(before.voice_channel, name=default_name)

            # If voice channel being left has no more members, reset to default name
            if before.voice_channel:
                if len(before.voice_channel.voice_members) == 0:
                    default_name = default_list[before.voice_channel.position]
                    await self.client.edit_channel(before.voice_channel, name=default_name)

    async def handle_voice_channel_update(self, before, after):
        await self._auto_rename_voice_channel(before, after)

    def _can_manage_server(self, user, channel):
        return channel.permissions_for(user).manage_server

    def _is_cakebot(self, user):
        return user.id == self.client.user.id

    def _is_owner(self, user):
        return str(user.id) == cakebot_config.OWNER_ID

