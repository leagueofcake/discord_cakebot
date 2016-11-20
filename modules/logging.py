def get_log_channel_id(c, server_id):
    c.execute("SELECT channel_id FROM log_channel WHERE server_id = ?", (server_id, ))
    return c.fetchone()


def add_log_channel(c, server_id, channel_id):
    c.execute("INSERT INTO log_channel(server_id, channel_id) VALUES (?, ?)", (server_id, channel_id))


def update_log_channel(c, server_id, channel_id):
    c.execute("UPDATE log_channel SET channel_id = ? WHERE server_id = ?", (channel_id, server_id))


def get_log_channel(c, server):
    for channel in server.channels:
        log_channel_id = get_log_channel_id(c, server.id)
        if log_channel_id:
            if channel.id == log_channel_id[0]:
                return channel
    return None
