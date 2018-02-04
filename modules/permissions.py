def get_permissions(c, user_id, server_id):
    c.execute("SELECT permissions FROM permissions WHERE user_id = ? AND server_id = ?", (user_id, server_id))
    return c.fetchone()


def set_permissions(c, user_id, server_id, new_perms):
    c.execute("INSERT INTO permissions (user_id, server_id, permissions) VALUES (?, ?, ?)",
              (user_id, server_id, ','.join(new_perms)))


def update_permissions(c, user_id, server_id, new_perms):
    c.execute("UPDATE permissions SET permissions = ? WHERE user_id = ? AND server_id = ?",
              (new_perms, user_id, server_id))

allowed_perm_commands = ['musicprefix', 'logchannel']
