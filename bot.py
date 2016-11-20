import asyncio
import sqlite3
import sys

import discord
import requests

import cakebot_config
import cakebot_help
from modules.helpers import parse_command_args, is_integer, temp_message
from modules.misc import return_troll
from modules.permissions import get_permissions, set_permissions, update_permissions, find_permissions
from modules.music import get_music_prefix, add_music_prefix, update_music_prefix

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
    if content.startswith('!hello'):
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    if content.startswith('!bye'):
        if str(message.author.id) == cakebot_config.OWNER_ID:
            await client.send_message(message.channel, 'Logging out, bye!')
            sys.exit()
        else:
            await client.send_message(message.channel, 'I\'m not going anywhere!')
    elif content.startswith('!permissions'):
        args = parse_command_args(content)

        # Gets permissions for mentioned user if given, otherwise defaults to calling user
        user = message.author
        if message.mentions:
            user = message.mentions[0]  # Find id of first mentioned user

        # await client.send_message(message.channel, 'Detected: {} with id {}'.format(user, user.id))

        perms = get_permissions(c, user.id, message.server.id)
        if len(args) == 1 or len(args) == 2:
            if perms:
                await client.send_message(message.channel, 'Permissions for {}: {}'.format(user, perms))
            else:
                await client.send_message(message.channel, 'There are no set permissions for: {}'.format(user))
        elif str(message.author.id) == cakebot_config.OWNER_ID and len(args) > 2:
            add_perms = args[2:]
            if perms:
                current_perms = perms[0]
                new_perms = current_perms + ',' + ','.join(add_perms)
                update_permissions(c, user.id, message.server.id, new_perms)
            else:
                set_permissions(c, user.id, message.server.id, add_perms)
            conn.commit()
            add_message = 'Added permissions: `{}` to {}'.format(','.join(add_perms), user)
            await client.send_message(message.channel, add_message)
    elif content.startswith('!musicprefix'):
        args = parse_command_args(content)
        perms = get_permissions(c, message.author.id, message.server.id)

        can_manage_server = message.channel.permissions_for(message.author).manage_server
        has_musicprefix_perm = find_permissions(perms, 'musicprefix')

        music_prefix = get_music_prefix(c, message.server.id)
        if len(args) == 1:
            if music_prefix:
                await temp_message(client, message.channel, 'Current music prefix for this server is: `{}`'.format(music_prefix[0]))
            else:
                await temp_message(client, message.channel, 'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')
        else:
            if can_manage_server or has_musicprefix_perm:
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
    elif content.startswith('!invite'):
        await client.send_message(message.channel, 'Add me to your server! Click here: {}!'.format(cakebot_config.NORMAL_INVITE_LINK))
    elif content.startswith('!timedcats'):
        if str(message.author.id) == cakebot_config.OWNER_ID:
            times = 5
            duration_str = 'm'

            args = parse_command_args(content)

            if len(args) > 1:
                arg_times = args[1]
                if is_integer(arg_times):
                    if int(arg_times) <= 60:
                        times = int(arg_times)

                if len(args) > 2:
                    arg_duration = args[2]
                    if arg_duration in cakebot_config.time_map:
                        duration_str = arg_duration

            unit_time = cakebot_config.time_map[duration_str][0]
            duration_time = unit_time * times

            unit_duration_str = cakebot_config.time_map[duration_str][1]
            long_duration_str = cakebot_config.time_map[duration_str][2]

            if times == 1:
                long_duration_str = unit_duration_str

            sending_msg = 'Sending cats every {} for {} {}!'.format(unit_duration_str, times, long_duration_str)
            await client.send_message(message.channel, sending_msg)

            loop = asyncio.get_event_loop()
            end_time = loop.time() + duration_time

            await asyncio.sleep(5)
            while True:
                cat_url = requests.get('http://random.cat/meow').json()['file']
                await client.send_message(message.channel, cat_url)
                if (loop.time() + unit_time) >= end_time:
                    break
                await(asyncio.sleep(unit_time))
            await client.send_message(message.channel, 'Finished sending cats!')
        else:
            await client.send_message(message.channel, 'Only leagueofcake can send cats right now, sorry :(')
    elif content.startswith('!find'):
        args = parse_command_args(content)
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
    elif content.startswith('!trollurl'):
        args = parse_command_args(content)
        url = args[1]
        await client.send_message(message.channel, return_troll(url))
        await client.delete_message(message)
    elif content.startswith('!google'):
        args = parse_command_args(content)
        words = args[1:]
        url = 'https://www.google.com/#q=' + '+'.join(words)
        await client.send_message(message.channel, url)
    elif content.startswith('!redirect'):
        args = parse_command_args(content)
        room = message.channel_mentions[0]
        await client.send_message(room, '`{}` redirected:'.format(message.author))
        await client.send_message(room, ' '.join(args[2:]))
        await client.delete_message(message)
    elif content.startswith('!play'): # Play song by title
        args = parse_command_args(content)
        if args[0] == '!play':
            song_name = ' '.join(args[1:])
            s = '%{}%'.format(song_name.lower())
            c.execute("SELECT * FROM songs WHERE LOWER(name) LIKE ? OR LOWER(alias) LIKE ?", (s, s))
            found = c.fetchmany(size=13)

            if len(found) == 1:
                server_id = message.server.id
                c.execute("SELECT prefix FROM music_prefix WHERE server_id = ?", (server_id, ))
                prefix = c.fetchone()
                if prefix:
                    prefix = prefix[0]
                    await temp_message(client, message.channel, '{} {}'.format(prefix, found[0][4]))
                    await client.send_message(message.channel, '{} queued: {}'.format(message.author, found[0][1]))
                else:
                    await temp_message(client, message.channel, 'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')
            elif len(found) > 1:
                results = "\nFound multiple matches: (limited to 13). Use ``!playid <id>``\n```"
                s = '%{}%'.format(song_name.lower())
                c.execute("SELECT * FROM songs WHERE LOWER(name) LIKE ? OR LOWER(alias) LIKE ?", (s, s))
                found = c.fetchmany(size=13)
                results += '{} {} {} {} {}'.format('ID'.ljust(4, ' '), 'Name'.ljust(45, ' '), 'Artist'.ljust(25, ' '), 'Album'.ljust(35, ' '), 'Alias'.ljust(20, ' '))
                if found:
                    for song in found:
                        id, name, artist, album, alias = song[0], song[1], song[2], song[3], song[5]
                        id = str(id).ljust(4, ' ')
                        name = name[:45].ljust(45, ' ')
                        artist = str(artist)[:25].ljust(25, ' ')
                        album = str(album)[:35].ljust(35, ' ')
                        alias = str(alias)[:20].ljust(20, ' ')

                        formatted = "{} {} {} {} {}".format(id, name, artist, album, alias)
                        results += '\n' + formatted
                    await temp_message(client, message.channel, results + '```', time=8)
            else:
                await client.send_message(message.channel, "Couldn't find that song!")
        else:
            if content.startswith('!playalbum'):
                album_name = ' '.join(args[1:])
                c.execute("SELECT * FROM songs WHERE LOWER(album) LIKE ?", ('%{}%'.format(album_name.lower()),))
            elif content.startswith('!playid'):
                id = args[1]
                c.execute("SELECT * FROM songs WHERE id LIKE ?", (id,))

            found = c.fetchmany(size=15)
            server_id = message.server.id

            if found:
                for song in found:
                    # await client.send_message(message.channel, found)
                    # Find music_prefix in db
                    c.execute("SELECT prefix FROM music_prefix WHERE server_id = ?", (server_id, ))
                    prefix = c.fetchone()
                    if prefix:
                        prefix = prefix[0]
                        await temp_message(client, message.channel, '{} {}'.format(prefix, song[4]), time=3)
                        await client.send_message(message.channel, '{} queued: {}'.format(message.author, song[1]))
                    else:
                        await temp_message(client, message.channel, 'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')
            else:
                await client.send_message(message.channel, "Couldn't find that song!")

    elif content.startswith('!reqsong'):
        await client.send_message(message.channel, '\nFill this in and PM leagueofcake: <http://goo.gl/forms/LesR4R9oXUalDRLz2>\nOr this (multiple songs): <http://puu.sh/pdITq/61897089c8.csv>')
    elif content.startswith('!search'):
        args = parse_command_args(content)
        search_str = ' '.join(args[1:])
        s = '%{}%'.format(search_str.lower())
        c.execute("SELECT * FROM songs WHERE LOWER(name) LIKE ? OR LOWER(album) LIKE ? OR LOWER(artist) LIKE ? OR LOWER(alias) LIKE ?", (s, s, s, s))
        found = c.fetchmany(size=13)
        results = '\nSongs found (limited to 13):\n```'
        results += '{} {} {} {} {}'.format('ID'.ljust(4, ' '), 'Name'.ljust(45, ' '), 'Artist'.ljust(25, ' '), 'Album'.ljust(35, ' '), 'Alias'.ljust(20, ' '))
        if found:
            for song in found:
                id, name, artist, album, alias = song[0], song[1], song[2], song[3], song[5]
                id = str(id).ljust(4, ' ')
                name = name[:45].ljust(45, ' ')
                artist = str(artist)[:25].ljust(25, ' ')
                album = str(album)[:35].ljust(35, ' ')
                alias = str(alias)[:20].ljust(20, ' ')

                formatted = "{} {} {} {} {}".format(id, name, artist, album, alias)
                results += '\n' + formatted
            await temp_message(client, message.channel, results + '```', time=8)
        else:
            await client.send_message(message.channel, "Couldn't find any songs!")
    elif content.startswith('!help'):
        args = parse_command_args(content)
        if len(args) > 1:  # specific command
            command = args[1]
            try:
                await temp_message(client, message.channel, cakebot_help.get_entry(command), time=10)
            except KeyError:
                await temp_message(client, message.channel, 'Command not found! Do ``!help`` for the command list.', time=10)
        else:  # command list summary
            await temp_message(client, message.channel, cakebot_help.generate_summary(), time=10)
    # elif content.startswith('!'):
        # await temp_message(client, message.channel, 'Unknown command! Type !help for commands')

client.run(cakebot_config.TOKEN)
