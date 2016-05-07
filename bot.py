import discord
import asyncio
import cakebot_config

client = discord.Client()
invite = 'https://discordapp.com/oauth2/authorize?client_id=178312661233172480&scope=bot&permissions=66186303'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await client.send_message(message.channel, 'Sleeping for 5 seconds!')
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping!')
    elif message.content.startswith('!hello'):
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    elif message.content.startswith('!'):
        await client.send_message(message.channel, 'Unknown command!')

client.run(cakebot_config.token)
