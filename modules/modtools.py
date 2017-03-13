from datetime import datetime
from .helpers import get_full_username, temp_message


def get_log_channel_id(c, server_id):
    c.execute("SELECT channel_id FROM log_channel WHERE server_id = ?", (server_id, ))
    res = c.fetchone()
    if res:
        return res[0]
    return None


def add_log_channel(c, server_id, channel_id):
    c.execute("INSERT INTO log_channel(server_id, channel_id) VALUES (?, ?)", (server_id, channel_id))


def update_log_channel(c, server_id, channel_id):
    c.execute("UPDATE log_channel SET channel_id = ? WHERE server_id = ?", (channel_id, server_id))


def gen_edit_message_log(before, after):
    before_content = before.clean_content
    after_content = after.clean_content
    local_message_time = datetime.now().strftime("%H:%M:%S")

    if before.attachments:
        before_content += ' ' + before.attachments[0]['proxy_url']
    if after.attachments:
        after_content += ' ' + after.attachments[0]['proxy_url']

    log_message = '[{}] {} *edited their message in* {}\n' \
                  'Before: {}\n' \
                  'After+: {}'.format(local_message_time, get_full_username(before.author), before.channel.mention,
                                      before_content, after_content)
    return log_message


def gen_delete_message_log(message):
    clean_content = message.clean_content
    local_message_time = datetime.now().strftime("%H:%M:%S")
    username = get_full_username(message.author)

    if message.attachments:
        clean_content += ' ' + message.attachments[0]['proxy_url']

    return '[{}] {} *deleted their message in* {}\n' \
           '{}'.format(local_message_time, username, message.channel.mention, clean_content)

async def purge_messages(message, client, user_id, num):
    if 1 <= num <= 100:
        to_delete = []
        async for log in client.logs_from(message.channel, limit=500):
            if log.author.id == user_id:
                to_delete.append(log)
            if len(to_delete) == num:  # Found num amount of messages
                break

        if len(to_delete) == 1:
            await client.delete_message(to_delete[0])
        else:
            await client.delete_messages(to_delete)
        await temp_message(client, message.channel,
                           "Purged {} messages from {}.".format(len(to_delete),
                                                                message.author))
    else:
        await client.send_message(message.channel,
                                  "Please specify a valid number of messages to purge.")