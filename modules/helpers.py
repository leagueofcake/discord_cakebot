import asyncio


def parse_command_args(command):
    return command.split(' ')


def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False


async def temp_message(client, channel, message, time=5):
    tmp = await client.send_message(channel, message)
    await asyncio.sleep(time)
    await client.delete_message(tmp)