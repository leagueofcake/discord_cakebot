import logging

import discord

import bot.cakebot_config as cakebot_config
from bot.Bot import Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

client = discord.Client()
bot = Bot(client, logger)
(
    bot.plug_in_module("core")
    .plug_in_module("permissions")
    .plug_in_module("modtools")
    .plug_in_module("messages")
    .plug_in_module("music")
    .plug_in_module("misc")
)


@client.event
async def on_ready():
    dashes = "-" * max(
        len("Logged in as"), len(client.user.name), len(str(client.user.id))
    )
    logger.info(dashes)
    logger.info("Logged in as")
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
async def on_guild_channel_update(before, after):
    await bot.handle_guild_channel_update(before, after)


@client.event
async def on_member_update(before, after):
    await bot.handle_member_update(before, after)


@client.event
async def on_voice_state_update(member, before, after):
    await bot.handle_voice_channel_update(member, before, after)


client.run(cakebot_config.TOKEN)
