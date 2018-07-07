import logging

import discord

import cakebot_config
from Bot import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

client = discord.Client()
bot = Bot(client, logger)
bot.load_module('core')
bot.load_module('permissions')
bot.load_module('modtools')
bot.load_module('messages')
bot.load_module('music')
bot.load_module('misc')


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
    await bot.handle_incoming_message(message)


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
