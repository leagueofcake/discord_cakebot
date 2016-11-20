def get_music_prefix(c, server_id):
    c.execute("SELECT prefix FROM music_prefix WHERE server_id = ?", (server_id, ))
    return c.fetchone()


def add_music_prefix(c, server_id, new_prefix):
    c.execute("INSERT INTO music_prefix(server_id, prefix) VALUES (?, ?)", (server_id, new_prefix))


def update_music_prefix(c, server_id, new_prefix):
    c.execute("UPDATE music_prefix SET prefix = ? WHERE server_id = ?", (new_prefix, server_id))