from datetime import datetime


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
    author = before.author
    before_content = before.clean_content
    after_content = after.clean_content
    local_message_time = datetime.now().strftime("%H:%M:%S")
    channel_name = before.channel.mention
    username = '{}#{}'.format(author.display_name, author.discriminator)

    if before.attachments:
        before_content += ' ' + before.attachments[0]['proxy_url']
    if after.attachments:
        after_content += ' ' + after.attachments[0]['proxy_url']

    log_message = '[{}] {} *edited their message in* {}\nBefore: {}\nAfter+: {}'.format(local_message_time, username,
                                                                                        channel_name, before_content,
                                                                                        after_content)
    return log_message


def gen_delete_message_log(message):
    author = message.author
    content = message.clean_content
    local_message_time = datetime.now().strftime("%H:%M:%S")
    channel_name = message.channel.mention
    username = '{}#{}'.format(author.display_name, author.discriminator)

    if message.attachments:
        content += ' ' + message.attachments[0]['proxy_url']

    log_message = '[{}] {} *deleted their message in* {}\n{}'.format(local_message_time, username, channel_name,
                                                                     content)
    return log_message
