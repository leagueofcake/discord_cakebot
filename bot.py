import asyncio
import sqlite3
import sys
import logging

import discord
import requests

import cakebot_config
import cakebot_help
from datetime import datetime
from modules.helpers import temp_message, is_integer, get_full_username
from modules.misc import return_troll, parse_duration_str
from modules.permissions import get_permissions, set_permissions, update_permissions, allowed_perm_commands
from modules.music import get_music_prefix, add_music_prefix, update_music_prefix, find_song_by_name, \
    find_album, find_song_by_id, search_songs, make_song_results, queue_songs
from modules.modtools import add_log_channel, update_log_channel, get_log_channel_id, gen_edit_message_log, \
    gen_delete_message_log, purge_messages, auto_rename_voice_channel


class Bot:
    def __init__(self, client):
        self.client = client

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

    async def auth_function(self, f):
        async def ret_fun(message, owner_auth=False, manage_server_auth=False, require_non_cakebot=False, cakebot_perm=None):
            owner_check = owner_auth and self._is_owner(message.author)
            manage_server_check = manage_server_auth and self._can_manage_server(message.author, message.channel)
            is_cakebot_check = (not require_non_cakebot) or (require_non_cakebot and not self._is_cakebot(message.author))

            perms = get_permissions(c, message.author.id, message.server.id)
            cakebot_perm_check = cakebot_perm and perms and cakebot_perm in perms

            if is_cakebot_check and (owner_check or manage_server_check or cakebot_perm_check):
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

        res = await self.auth_function(inner)
        await res(message, owner_auth=True)

    async def _print_permissions(self, message, user):
        perms = get_permissions(c, user.id, message.server.id)
        if perms:
            perm_message = 'Permissions for {}: {}'.format(user, perms)
        else:
            perm_message = 'There are no set permissions for: {}'.format(user)
        if self._can_manage_server(user, message.channel):
            perm_message += '\nThis user has manage_server permissions.'

        await self.say(message.channel, perm_message)

    async def _set_permissions(self, message, user):
        async def inner(m):
            perms = get_permissions(c, user.id, m.server.id)
            add_perms = [comm for comm in m.content.split()[2:] if comm in allowed_perm_commands]  # Filter allowed permission commands

            if add_perms:
                if perms:
                    current_perms = perms[0]
                    new_perms = current_perms + ',' + ','.join(add_perms)
                    update_permissions(c, user.id, m.server.id, new_perms)
                else:
                    set_permissions(c, user.id, m.server.id, add_perms)
                conn.commit()
                add_message = 'Added permissions: `{}` to {}'.format(','.join(add_perms), user)
                await self.say(m.channel, add_message)
            else:
                await self.say(m.channel, 'No permissions were added to {}!'.format(user))
        res = await self.auth_function(inner)
        await res(message, require_non_cakebot=True, manage_server_auth=True, owner_auth=True)

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

            await bot.say(m.channel, 'Sending cats every {} for {} {}!'.format(unit, times, unit_plural))

            for i in range(times):
                cat_url = requests.get('http://random.cat/meow').json()['file']
                await bot.say(m.channel, cat_url)
                if i == times - 1:
                    await bot.say(m.channel, 'Finished sending cats!')
                    break
                await asyncio.sleep(unit_time)
        res = await self.auth_function(inner)
        await res(message, owner_auth=True)

    async def troll_url(self, message):
        await self.say(message.channel, return_troll(message.content.split()[1]))
        await self.delete(message)

    async def redirect(self, message):
        room = message.channel_mentions[0]
        await self.say(room, '`{}` redirected:'.format(message.author))
        await self.say(room, ' '.join(message.content.split()[2:]))
        await self.client.delete_message(message)

    async def purge(self, message):
        async def inner(m):
            args = m.content.split()

            await self.delete(m)
            if len(args) < 2:
                await bot.say(m.channel, "Please specify the number of messages to purge.")
            else:
                if m.mentions and len(args) >= 3:
                    purge_user = m.mentions[0]  # Find id of first mentioned user
                    if not is_integer(args[2]):
                        await bot.say(m.channel, "Please specify a valid number of messages to purge. (1-100)")
                    else:
                        num = int(args[2])
                        await purge_messages(message=message, client=self.client, purge_user=purge_user, num=num)
                else:
                    if not is_integer(args[1]):
                        await bot.say(m.channel, "Please specify a valid number of messages to purge. (1-100)")
                    else:
                        num = int(args[1])
                        try:
                            deleted = await self.client.purge_from(m.channel, limit=num)
                            await self.temp_message(m.channel, "Purged {} messages.".format(len(deleted)))
                        except discord.errors.HTTPException:  # Delete individually
                            async for log in self.client.logs_from(m.channel, limit=num):
                                await self.delete(log)

        res = await self.auth_function(inner)
        await res(message, manage_server_auth=True, require_non_cakebot=True)

    async def del_user_messages(self, message):
        async def inner(m):
            args = message.content.split()
            if len(args) == 1 or (len(args) == 2 and is_integer(args[1]) and args[1] == '1'):
                await self.delete(message)
                async for log in self.client.logs_from(message.channel, limit=500):
                    if log.author.id == message.author.id:
                        await self.delete(log)
                        break
            elif len(args) == 2:
                await self.delete(message)
                purge_user_id = message.author
                if not is_integer(args[1]):
                    await bot.say(message.channel, "Please specify a valid number of messages to delete. (1-100)")
                else:
                    num = int(args[1])
                    await purge_messages(message=message, client=self.client, purge_user=purge_user_id, num=num)
        res = await self.auth_function(inner)
        await res(message, require_non_cakebot=True)

    async def _print_log_channel(self, message):
        log_channel = self.client.get_channel(get_log_channel_id(c, message.server.id))
        if log_channel:
            await self.temp_message(message.channel, 'Log channel is: {}'.format(log_channel.mention))
        else:
            await self.temp_message(message.channel, 'No log channel configured! Add one with `!logchannel set`')

    async def _set_log_channel(self, message):
        async def inner(m):
            log_channel = self.client.get_channel(get_log_channel_id(c, m.server.id))
            if log_channel:
                update_log_channel(c, m.server.id, m.channel.id)
            else:
                add_log_channel(c, m.server.id, m.channel.id)
            await bot.say(m.channel, 'Set {} as the log channel!'.format(m.channel.mention))
            conn.commit()
        res = await self.auth_function(inner)
        await res(message, manage_server_auth=True, cakebot_perm='logchannel', require_non_cakebot=True)

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

    def _can_manage_server(self, user, channel):
        return channel.permissions_for(user).manage_server

    def _is_cakebot(self, user):
        return user.id == self.client.user.id

    def _is_owner(self, user):
        return str(user.id) == cakebot_config.OWNER_ID


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

client = discord.Client()
bot = Bot(client)
conn = sqlite3.connect(cakebot_config.DB_PATH)
c = conn.cursor()


@client.event
async def on_ready():
    logger.info('Logged in as')
    logger.info(client.user.name)
    logger.info(client.user.id)
    logger.info('------')


@client.event
async def on_message(message):
    args = message.content.split()
    command = args[0]

    is_cakebot = message.author.id == client.user.id

    if command == '!hello':
        await bot.hello(message)
    elif command == '!bye':
        await bot.bye(message)
    elif command == '!permissions':
        await bot.permissions(message)
    elif command == '!musicprefix':
        perms = get_permissions(c, message.author.id, message.server.id)
        can_manage_server = message.channel.permissions_for(message.author).manage_server
        has_musicprefix_perm = perms and 'musicprefix' in perms

        music_prefix = get_music_prefix(c, message.server.id)
        if len(args) == 1:
            if music_prefix:
                await temp_message(client, message.channel, 'Current music prefix for this server is: `{}`'.format(music_prefix))
            else:
                await temp_message(client, message.channel, 'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')
        else:
            if (can_manage_server or has_musicprefix_perm) and not is_cakebot:
                new_prefix = ' '.join(args[1:])
                if music_prefix:
                    update_music_prefix(c, message.server.id, new_prefix)
                    await bot.say(message.channel, 'Updated music prefix for this server to: `{}'.format(new_prefix))
                else:
                    add_music_prefix(c, message.server.id, new_prefix)
                    await bot.say(message.channel, 'Set music prefix for this server to: `{}`'.format(new_prefix))
                conn.commit()
            else:
                await temp_message(client, message.channel, 'You don\'t have the permissions to do that! Message a moderator to change it.')
    elif command == '!invite':
        await bot.say(message.channel, 'Add me to your server! Click here: {}'.format(cakebot_config.NORMAL_INVITE_LINK))
    elif command == '!timedcats':
        await bot.timed_cats(message)
    elif command == '!trollurl':
        await bot.troll_url(message)
    elif command == '!google':
        url = 'https://www.google.com/#q=' + '+'.join(args[1:])
        await bot.say(message.channel, url)
    elif command == '!redirect':
        await bot.redirect(message)
    elif command.startswith('!play') or command == '!search':  # Play song by title/alias
        prefix = get_music_prefix(c, message.server.id)
        if command == '!play' or command == '!search':
            search = '%{}%'.format(' '.join(args[1:]).lower())
            if command == '!play':
                found = find_song_by_name(c, search)
            elif command == '!search':
                found = search_songs(c, search)

            if len(found) == 1 and command == '!play':
                await queue_songs(client, message, prefix, found)
            elif len(found) > 1 or command == '!search':
                tmp = await bot.say(message.channel, make_song_results(found))

                def check(msg):
                    splitted = msg.content.split()
                    return len(splitted) >= 2 and splitted[0] == '!page' and is_integer(splitted[1])

                msg = await client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                while msg is not None:
                    await client.delete_message(msg)
                    await client.delete_message(tmp)

                    page_num = msg.content.split()[1]
                    tmp = await bot.say(message.channel, make_song_results(found, (int(page_num) - 1) * 13))
                    msg = await client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                await asyncio.sleep(cakebot_config.MUSIC_SEARCH_RESULT_TIME)
                await client.delete_message(tmp)
        else:
            found = None
            if command == '!playalbum':
                found = find_album(c, ' '.join(args[1:]))
                await bot.say(message.channel, "Queueing the following songs. Confirm with ``!yes`` or refine your search terms.")

                def check(msg):
                    splitted = msg.content.split()
                    return msg.content == '!yes' or (len(splitted) >= 2 and splitted[0] == '!page' and is_integer(splitted[1]))

                tmp = await bot.say(message.channel, make_song_results(found))
                msg = await client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                while msg is not None:
                    await client.delete_message(msg)
                    await client.delete_message(tmp)

                    if msg.content == '!yes':
                        await queue_songs(client, message, prefix, found)
                        break

                    page_num = msg.content.split()[1]
                    tmp = await bot.say(message.channel, make_song_results(found, (int(page_num) - 1) * 13))
                    msg = await client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)


                await asyncio.sleep(cakebot_config.MUSIC_SEARCH_RESULT_TIME)
                await client.delete_message(tmp)
            elif command == '!playid':
                found = find_song_by_id(c, args[1])
                await queue_songs(client, message, prefix, found)

        if not found:
            await bot.say(message.channel, "Couldn't find any matching songs!")
    elif command == '!reqsong':
        await bot.say(message.channel, 'Fill this in and PM leagueofcake: <http://goo.gl/forms/LesR4R9oXUalDRLz2>\nOr this (multiple songs): <http://puu.sh/pdITq/61897089c8.csv>')
    elif command == '!help':
        await bot.help(message)
    elif command == '!logchannel':
        await bot.log_channel(message)
    elif command == '!purge':
        await bot.purge(message)
    elif command == '!del':
        await bot.del_user_messages(message)
    elif command == '!say':
        await bot.say_in_room(message)
    # elif command == '!':
        # await temp_message(client, message.channel, 'Unknown command! Type !help for commands')


# Logging functionality
@client.event
async def on_message_edit(before, after):
    log_channel = client.get_channel(get_log_channel_id(c, before.server.id))
    if log_channel and before.content != after.content:
        await bot.say(log_channel, gen_edit_message_log(before, after))


@client.event
async def on_message_delete(message):
    log_channel = client.get_channel(get_log_channel_id(c, message.server.id))

    if log_channel:
        await bot.say(log_channel, gen_delete_message_log(message))


@client.event
async def on_channel_update(before, after):
    log_channel = client.get_channel(get_log_channel_id(c, before.server.id))

    if log_channel:
        local_message_time = datetime.now().strftime("%H:%M:%S")

        channel_mention = before.mention
        if before.name != after.name:
            message = '[{}] {} *changed channel name*\n' \
                          'Before: {}\n' \
                          'After+: {}'.format(local_message_time, channel_mention, before.name, after.name)
            await bot.say(log_channel, message)
        if before.topic != after.topic:
            message = '[{}] {} *changed topic contents*\n' \
                      'Before: {}\n' \
                      'After+: {}'.format(local_message_time, channel_mention, before.topic, after.topic)
            await bot.say(log_channel, message)


@client.event
async def on_member_update(before, after):
    log_channel = client.get_channel(get_log_channel_id(c, before.server.id))

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
            await bot.say(log_channel, message)

        elif before_roles != after_roles:
            message = '[{}] {} *changed roles*\n' \
                      'Before: {}\n' \
                      'After+: {}'.format(local_message_time, get_full_username(before),
                                          before_roles,
                                          after_roles)
            await bot.say(log_channel, message)

    if before.game != after.game:
        await auto_rename_voice_channel(client, before, after)


@client.event
async def on_voice_state_update(before, after):
    await auto_rename_voice_channel(client, before, after)

client.run(cakebot_config.TOKEN)
