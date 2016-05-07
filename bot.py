import discord
import asyncio
import cakebot_config

client = discord.Client()
invite = 'https://discordapp.com/oauth2/authorize?client_id=178312661233172480&scope=bot&permissions=66186303'

@client.event
async def on_server_join(server):
    channels = client.get_all_channels()
    for channel in channels:
        if str(channel.type) == 'text':
            await client.send_message(channel, 'Hi everyone!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    channels = client.get_all_channels()
    for channel in channels:
        if str(channel.type) == 'text':
            await client.send_message(channel, 'Hi everyone! I\'m online now!')

@client.event
async def on_message(message):
    content = message.content

    if content.startswith('!hello'):
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    elif content.startswith('!help'):
        tmp = await client.send_message(message.channel, cakebot_config.help_text)
    elif content.startswith('!'):
        tmp = await client.send_message(message.channel, 'Unknown command! Type !help for commands')
        await(asyncio.sleep(5))
        await client.delete_message(tmp)

client.run(cakebot_config.token)
