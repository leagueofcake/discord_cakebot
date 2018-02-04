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
from modules.permissions import get_permissions, set_permissions, update_permissions, find_permissions, \
    allowed_perm_commands
from modules.music import get_music_prefix, add_music_prefix, update_music_prefix, find_song_by_name, \
    find_album, find_song_by_id, search_songs, make_song_results, queue_songs
from modules.modtools import add_log_channel, update_log_channel, get_log_channel_id, gen_edit_message_log, \
    gen_delete_message_log, purge_messages, auto_rename_voice_channel


class Bot:
    def __init__(self, client):
        self.client = client

    def start(self):
        client.start()

    async def say(self, channel, message):
        await self.client.send_message(channel, message)


logging.basicConfig(level=logging.INFO)

client = discord.Client()
bot = Bot(client)
conn = sqlite3.connect(cakebot_config.DB_PATH)
c = conn.cursor()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    content = message.content
    args = content.split()
    command = args[0]

    is_cakebot = message.author.id == client.user.id

    if command == '!hello':
        await bot.say(message.channel, 'Hello {}!'.format(message.author.mention))
    elif command == '!bye':
        if str(message.author.id) == cakebot_config.OWNER_ID:
            await bot.say(message.channel, 'Logging out, bye!')
            sys.exit()
        else:
            await bot.say(message.channel, 'I\'m not going anywhere!')
    elif command == '!permissions':
        # Gets permissions for mentioned user if given, otherwise defaults to calling user
        user = message.author
        if message.mentions:
            user = message.mentions[0]  # Find id of first mentioned user

        can_manage_server = message.channel.permissions_for(user).manage_server
        is_owner = str(message.author.id) == cakebot_config.OWNER_ID
        perms = get_permissions(c, user.id, message.server.id)
        if len(args) == 1 or len(args) == 2:
            if perms:
                perm_message = 'Permissions for {}: {}'.format(user, perms)
            else:
                perm_message = 'There are no set permissions for: {}'.format(user)
            if can_manage_server:
                perm_message += '\nThis user has manage_server permissions.'
            await bot.say(message.channel, perm_message)
        elif (can_manage_server or is_owner) and len(args) > 2 and not is_cakebot:
            add_perms = [comm for comm in args[2:] if comm in allowed_perm_commands]  # Filter allowed permission commands

            if add_perms:
                if perms:
                    current_perms = perms[0]
                    new_perms = current_perms + ',' + ','.join(add_perms)
                    update_permissions(c, user.id, message.server.id, new_perms)
                else:
                    set_permissions(c, user.id, message.server.id, add_perms)
                conn.commit()
                add_message = 'Added permissions: `{}` to {}'.format(','.join(add_perms), user)
                await bot.say(message.channel, add_message)
            else:
                await bot.say(message.channel, 'No permissions were added to {}!'.format(user))
    elif command == '!musicprefix':
        perms = get_permissions(c, message.author.id, message.server.id)
        can_manage_server = message.channel.permissions_for(message.author).manage_server
        has_musicprefix_perm = find_permissions(perms, 'musicprefix')

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
                    bot.say(message.channel, 'Updated music prefix for this server to: `{}'.format(new_prefix))
                else:
                    add_music_prefix(c, message.server.id, new_prefix)
                    bot.say(message.channel, 'Set music prefix for this server to: `{}`'.format(new_prefix))
                conn.commit()
            else:
                await temp_message(client, message.channel, 'You don\'t have the permissions to do that! Message a moderator to change it.')
    elif command == '!invite':
        bot.say(message.channel, 'Add me to your server! Click here: {}'.format(cakebot_config.NORMAL_INVITE_LINK))
    elif command == '!timedcats':
        if str(message.author.id) == cakebot_config.OWNER_ID:
            times, duration_str = parse_duration_str(args)
            unit_time = cakebot_config.time_map[duration_str][0]

            unit_duration_str = cakebot_config.time_map[duration_str][1]
            long_duration_str = cakebot_config.time_map[duration_str][2]

            if times == 1:
                long_duration_str = unit_duration_str

            sending_msg = 'Sending cats every {} for {} {}!'.format(unit_duration_str, times, long_duration_str)
            bot.say(message.channel, sending_msg)

            for i in range(times):
                cat_url = requests.get('http://random.cat/meow').json()['file']
                await bot.say(message.channel, cat_url)
                if i == times - 1:
                    await bot.say(message.channel, 'Finished sending cats!')
                    break
                await asyncio.sleep(unit_time)
        else:
            await bot.say(message.channel, 'Only leagueofcake can send cats right now, sorry :(')
    elif command == '!trollurl':
        await bot.say(message.channel, return_troll(args[1]))
        await client.delete_message(message)
    elif command == '!google':
        url = 'https://www.google.com/#q=' + '+'.join(args[1:])
        await bot.say(message.channel, url)
    elif command == '!redirect':
        room = message.channel_mentions[0]
        await bot.say(room, '`{}` redirected:'.format(message.author))
        await bot.say(room, ' '.join(args[2:]))
        await client.delete_message(message)
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
        if len(args) > 1:  # specific command
            command = args[1]
            try:
                await temp_message(client, message.channel, cakebot_help.get_entry(command), time=10)
            except KeyError:
                await temp_message(client, message.channel, 'Command not found! Do ``!help`` for the command list.', time=10)
        else:  # command list summary
            await temp_message(client, message.channel, cakebot_help.generate_summary(), time=10)
    elif command == '!logchannel':
        perms = get_permissions(c, message.author.id, message.server.id)
        can_manage_server = message.channel.permissions_for(message.author).manage_server
        has_logchannel_perm = find_permissions(perms, 'logchannel')

        log_channel = client.get_channel(get_log_channel_id(c, message.server.id))
        if len(args) == 1:
            if log_channel:
                await temp_message(client, message.channel,
                                   'Log channel is: {}'.format(log_channel.mention))
            else:
                await temp_message(client, message.channel,
                                   'No log channel configured! Add one with `!logchannel set`')
        else:
            if len(args) == 2:
                if args[1] == 'set':
                    if (can_manage_server or has_logchannel_perm) and not is_cakebot:
                        if log_channel:
                            update_log_channel(c, message.server.id, message.channel.id)
                        else:
                            add_log_channel(c, message.server.id, message.channel.id)
                        await bot.say(message.channel, 'Set {} as the log channel!'.format(message.channel.mention))
                        conn.commit()
                    else:
                        await temp_message(client, message.channel,
                                           'You don\'t have the permissions to do that! Message a moderator to change it.')
    elif command == '!purge':
        can_manage_server = message.channel.permissions_for(message.author).manage_server

        if can_manage_server and not is_cakebot:
            await client.delete_message(message)
            if len(args) < 2:
                await bot.say(message.channel, "Please specify the number of messages to purge.")
            else:
                if message.mentions and len(args) >= 3:
                    purge_user = message.mentions[0]  # Find id of first mentioned user
                    if not is_integer(args[2]):
                        await bot.say(message.channel, "Please specify a valid number of messages to purge. (1-100)")
                    else:
                        num = int(args[2])
                        await purge_messages(message=message, client=client, purge_user=purge_user, num=num)
                else:
                    if not is_integer(args[1]):
                        await bot.say(message.channel, "Please specify a valid number of messages to purge. (1-100)")
                    else:
                        num = int(args[1])
                        deleted = await client.purge_from(message.channel, limit=num)
                        await temp_message(client, message.channel, "Purged {} messages.".format(len(deleted)))

        else:
            await bot.say(message.channel, "You don't have the permissions to do that!")
    elif command == '!del':
        if not is_cakebot:
            if len(args) == 1 or (len(args) == 2 and is_integer(args[1]) and args[1] == '1'):
                await client.delete_message(message)
                async for log in client.logs_from(message.channel, limit=500):
                    if log.author.id == message.author.id:
                        await client.delete_message(log)
                        break
            elif len(args) == 2:
                await client.delete_message(message)
                purge_user_id = message.author
                if not is_integer(args[1]):
                    await bot.say(message.channel, "Please specify a valid number of messages to delete. (1-100)")
                else:
                    num = int(args[1])
                    await purge_messages(message=message, client=client, purge_user=purge_user_id, num=num)
    elif command == '!bookmark':
        if not is_cakebot:
            await client.delete_message(message)
            label = ' '.join(args[1:])
            if label:
                await bot.say(message.channel, '{} Bookmark: {}'.format(message.author.mention, label))
            else:
                await bot.say(message.channel, '{} Bookmark created.'.format(message.author.mention, label))
    elif command == '!bot.say':
        is_owner = str(message.author.id) == cakebot_config.OWNER_ID
        if not is_cakebot and is_owner:
            room = message.channel_mentions[0]
            if room:
                await bot.say(room, ' '.join(args[2:]))
            else:
                await bot.say(room, 'No room specified!')
            await client.delete_message(message)
        else:
            await bot.say('Only the owner of the bot can use this!')
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
