import discord
import asyncio
import requests
import cakebot_config

client = discord.Client()
invite = 'https://discordapp.com/oauth2/authorize?client_id=178312661233172480&scope=bot&permissions=66186303'

def parse_command_args(command):
    splitted = command.split(' ')
    if len(splitted) >= 2:
        return splitted[1]
    return None

def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

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
    elif content.startswith('!timedcats'):
        duration = 5
        args = parse_command_args(content)
        if is_integer(args):
            if int(args) <= 60:
                duration = int(args)

        await client.send_message(message.channel, 'Sending cats every minute for {} minutes!'.format(duration))
        loop = asyncio.get_event_loop()
        end_time = loop.time() + 60 * duration

        while True:
            cat_url = requests.get('http://random.cat/meow').json()['file']
            await client.send_message(message.channel, cat_url)
            if (loop.time() + 60) >= end_time:
                break
            await(asyncio.sleep(60))
        await client.send_message(message.channel, 'Finished sending cats!')
    elif content.startswith('!help'):
        tmp = await client.send_message(message.channel, cakebot_config.help_text)
        await(asyncio.sleep(5))
        await client.delete_message(tmp)
    elif content.startswith('!'):
        tmp = await client.send_message(message.channel, 'Unknown command! Type !help for commands')
        await(asyncio.sleep(5))
        await client.delete_message(tmp)

client.run(cakebot_config.token)
