import logging

import discord

import cakebot_config
from Bot import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

client = discord.Client()
bot = Bot(client, logger)
bot.plug_in_module('permissions')
bot.plug_in_module('messages')
bot.plug_in_module('music')
bot.plug_in_module('misc')


@client.event
async def on_ready():
    dashes = '-' * max(len('Logged in as'), len(client.user.name), len(client.user.id))
    logger.info(dashes)
    logger.info('Logged in as')
    logger.info(client.user.name)
    logger.info(client.user.id)
    logger.info(dashes)


@client.event
async def on_message(message):
    args = message.content.split()
    command = args[0]

    if command == '!hello':
        await bot.hello(message)
    elif command == '!bye':
        await bot.bye(message)
    elif command == '!permissions':
        await bot.permissions(message)
    elif command == '!musicprefix':
        await bot.music_prefix(message)
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
        await bot.search_and_play(message)
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
    await bot.handle_edited_message(before, after)

@client.event
async def on_message_delete(message):
    await bot.handle_deleted_message(message)

@client.event
async def on_channel_update(before, after):
    await bot.handle_channel_update(before, after)


@client.event
async def on_member_update(before, after):
    await bot.handle_member_update(before, after)

@client.event
async def on_voice_state_update(before, after):
    await bot.handle_voice_channel_update(before, after)

client.run(cakebot_config.TOKEN)
