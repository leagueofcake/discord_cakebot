import discord
import asyncio
import requests
import cakebot_config

client = discord.Client()
invite = 'https://discordapp.com/oauth2/authorize?client_id=178312661233172480&scope=bot&permissions=66186303'

def parse_command_args(command):
    splitted = command.split(' ')
    if len(splitted) >= 2:
        return splitted[1:]
    return None

def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

# @client.event
# async def on_server_join(server):
#     pass
#     channels = client.get_all_channels()
#     for channel in channels:
#         if str(channel.type) == 'text':
#             await client.send_message(channel, 'Hi everyone!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # channels = client.get_all_channels()
    # for channel in channels:
    #     if str(channel.type) == 'text':
    #         await client.send_message(channel, 'Hi everyone! I\'m online now!')

@client.event
async def on_message(message):
    content = message.content
    if content.startswith('!hello'):
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    elif content.startswith('!timedcats'):
        if str(message.author) == 'leagueofcake#5979':
            times = 5
            duration_str = 'm'

            args = parse_command_args(content)

            if len(args) > 0:
                arg_times = args[0]
                if is_integer(arg_times):
                    if int(arg_times) <= 60:
                        times = int(arg_times)

                if len(args) > 1:
                    arg_duration = args[1]
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
        await client.delete_message(tmp)
    # elif content.startswith('!help'):
        # tmp = await client.send_message(message.channel, cakebot_config.help_text)
        # await(asyncio.sleep(5))
        # await client.delete_message(tmp)
    # elif content.startswith('!'):
        # tmp = await client.send_message(message.channel, 'Unknown command! Type !help for commands')
        # await(asyncio.sleep(5))
        # await client.delete_message(tmp)

client.run(cakebot_config.token)
