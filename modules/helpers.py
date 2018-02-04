import asyncio


def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False


# Returns a string in the form username#descriptor e.g. Clyde#1234
def get_full_username(user):
    return '{}#{}'.format(user.name, user.discriminator)

# @TODO delete (superceded by Bot.temp_message)
async def temp_message(client, channel, message, time=5):
    tmp = await client.send_message(channel, message)
    await asyncio.sleep(time)
    await client.delete_message(tmp)
