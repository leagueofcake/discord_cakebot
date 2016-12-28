import asyncio
import sqlite3
import sys
import logging

import discord
import requests

import cakebot_config
import cakebot_help
from modules.helpers import temp_message, is_integer
from modules.misc import return_troll, parse_duration_str
from modules.permissions import get_permissions, set_permissions, update_permissions, find_permissions, \
    allowed_perm_commands
from modules.music import get_music_prefix, add_music_prefix, update_music_prefix, find_song_by_name, \
    find_album, find_song_by_id, search_songs, make_song_results, queue_songs
from modules.modtools import add_log_channel, update_log_channel, get_log_channel_id, gen_edit_message_log, \
    gen_delete_message_log

logging.basicConfig(level=logging.INFO)

client = discord.Client()
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
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    if command == '!bye':
        if str(message.author.id) == cakebot_config.OWNER_ID:
            await client.send_message(message.channel, 'Logging out, bye!')
            sys.exit()
        else:
            await client.send_message(message.channel, 'I\'m not going anywhere!')
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
            await client.send_message(message.channel, perm_message)
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
                await client.send_message(message.channel, add_message)
            else:
                await client.send_message(message.channel, 'No permissions were added to {}!'.format(user))
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
                    await client.send_message(message.channel, 'Updated music prefix for this server to: `{}`'.format(new_prefix))
                else:
                    add_music_prefix(c, message.server.id, new_prefix)
                    await client.send_message(message.channel, 'Set music prefix for this server to: `{}`'.format(new_prefix))
                conn.commit()
            else:
                await temp_message(client, message.channel, 'You don\'t have the permissions to do that! Message a moderator to change it.')
    elif command == '!invite':
        await client.send_message(message.channel, 'Add me to your server! Click here: {}'.format(cakebot_config.NORMAL_INVITE_LINK))
    elif command == '!timedcats':
        if str(message.author.id) == cakebot_config.OWNER_ID:
            times, duration_str = parse_duration_str(args)
            unit_time = cakebot_config.time_map[duration_str][0]

            unit_duration_str = cakebot_config.time_map[duration_str][1]
            long_duration_str = cakebot_config.time_map[duration_str][2]

            if times == 1:
                long_duration_str = unit_duration_str

            sending_msg = 'Sending cats every {} for {} {}!'.format(unit_duration_str, times, long_duration_str)
            await client.send_message(message.channel, sending_msg)

            for i in range(times):
                cat_url = requests.get('http://random.cat/meow').json()['file']
                await client.send_message(message.channel, cat_url)
                if i == times - 1:
                    await client.send_message(message.channel, 'Finished sending cats!')
                    break
                await asyncio.sleep(unit_time)
        else:
            await client.send_message(message.channel, 'Only leagueofcake can send cats right now, sorry :(')
    elif command == '!find':
        found = False

        if len(args) > 1:
            keyword = args[1]
            user_id = None
            if message.raw_mentions:
                user_id = message.raw_mentions[0]  # Find id of first mentioned user

            async for log in client.logs_from(message.channel, limit=500):
                if keyword.lower() in log.content.lower() and log.id != message.id and log.author != client.user:
                    if user_id is None or log.author.id == user_id:
                        try:
                            timestamp = log.timestamp.strftime('%H:%M, %d/%m/%Y')
                            await client.send_message(message.channel, '{} said at {}:\n```{}```'.format(log.author, timestamp, log.clean_content))
                            found = True
                        except:
                            print('Untranslatable message')
                        break  # terminate after finding first message
            if not found:
                await temp_message(client, message.channel, 'Couldn\'t find message!')
        else:
            await client.send_message(message.channel, 'Not enough arguments! Expecting 1')
    elif command == '!trollurl':
        await client.send_message(message.channel, return_troll(args[1]))
        await client.delete_message(message)
    elif command == '!google':
        url = 'https://www.google.com/#q=' + '+'.join(args[1:])
        await client.send_message(message.channel, url)
    elif command == '!redirect':
        room = message.channel_mentions[0]
        await client.send_message(room, '`{}` redirected:'.format(message.author))
        await client.send_message(room, ' '.join(args[2:]))
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
            elif len(found) > 1:
                tmp = await client.send_message(message.channel, make_song_results(found))

                def check(msg):
                    splitted = msg.content.split()
                    return len(splitted) >= 2 and splitted[0] == '!page' and is_integer(splitted[1])

                msg = await client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                while msg is not None:
                    await client.delete_message(msg)
                    await client.delete_message(tmp)

                    page_num = msg.content.split()[1]
                    tmp = await client.send_message(message.channel, make_song_results(found, (int(page_num) - 1) * 13))
                    msg = await client.wait_for_message(author=message.author, check=check, timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                await asyncio.sleep(cakebot_config.MUSIC_SEARCH_RESULT_TIME)
                await client.delete_message(tmp)
        else:
            found = None
            if command == '!playalbum':
                found = find_album(c, ' '.join(args[1:]))
            elif command == '!playid':
                found = find_song_by_id(c, args[1])
            await queue_songs(client, message, prefix, found)

        if not found:
            await client.send_message(message.channel, "Couldn't find any matching songs!")
    elif command == '!reqsong':
        await client.send_message(message.channel, 'Fill this in and PM leagueofcake: <http://goo.gl/forms/LesR4R9oXUalDRLz2>\nOr this (multiple songs): <http://puu.sh/pdITq/61897089c8.csv>')
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
                        await client.send_message(message.channel, 'Set {} as the log channel!'.format(message.channel.mention))
                        conn.commit()
                    else:
                        await temp_message(client, message.channel,
                                           'You don\'t have the permissions to do that! Message a moderator to change it.')
    elif command == '!purge':
        can_manage_server = message.channel.permissions_for(message.author).manage_server

        if can_manage_server and not is_cakebot:
            await client.delete_message(message)
            if len(args) < 2:
                await client.send_message(message.channel, "Please specify the number of messages to purge.")
            else:
                if message.mentions and len(args) >= 3:
                    purge_user_id = message.mentions[0].id  # Find id of first mentioned user
                    if not is_integer(args[2]):
                        await client.send_message(message.channel, "Please specify a valid number of messages to purge.")
                    else:
                        num = int(args[2])
                        if 1 <= num <= 100:
                            to_delete = []
                            async for log in client.logs_from(message.channel, limit=500):
                                if log.author.id == purge_user_id:
                                    to_delete.append(log)
                                if len(to_delete) == num:  # Found num amount of messages
                                    break

                            if len(to_delete) == 1:
                                await client.delete_message(to_delete[0])
                            else:
                                await client.delete_messages(to_delete)
                            await temp_message(client, message.channel, "Purged {} messages from {}.".format(len(to_delete), message.mentions[0]))
                        else:
                            await client.send_message(message.channel, "Please specify a valid number of messages to purge.")
                else:
                    if not is_integer(args[1]):
                        await client.send_message(message.channel, "Please specify a valid number of messages to purge.")
                    else:
                        num = int(args[1])
                        deleted = await client.purge_from(message.channel, limit=num)
                        await temp_message(client, message.channel, "Purged {} messages.".format(len(deleted)))

        else:
            await client.send_message(message.channel, "You don't have the permissions to do that!")
    elif content.strip() == '!del':
        if not is_cakebot:
            await client.delete_message(message)
            async for log in client.logs_from(message.channel, limit=500):
                if log.author.id == message.author.id:
                    await client.delete_message(log)
                    break

    # elif command == '!':
        # await temp_message(client, message.channel, 'Unknown command! Type !help for commands')


# Logging functionality
@client.event
async def on_message_edit(before, after):
    log_channel = client.get_channel(get_log_channel_id(c, before.server.id))
    if log_channel and before.content != after.content:
        await client.send_message(log_channel, gen_edit_message_log(before, after))


@client.event
async def on_message_delete(message):
    log_channel = client.get_channel(get_log_channel_id(c, message.server.id))

    if log_channel:
        await client.send_message(log_channel, gen_delete_message_log(message))


client.run(cakebot_config.TOKEN)
