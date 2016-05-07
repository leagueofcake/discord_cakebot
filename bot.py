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

client.run(cakebot_config.token)
