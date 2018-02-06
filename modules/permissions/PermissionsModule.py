import cakebot_config
from modules.ModuleInterface import ModuleInterface
from modules.permissions import permissions_help


class PermissionsModule(ModuleInterface):
    allowed_perm_commands = ['musicprefix', 'logchannel']

    def auth_function(self, f):
        async def ret_fun(message, owner_auth=False, manage_server_auth=False, require_non_cakebot=False,
                          cakebot_perm=None):
            owner_check = owner_auth and self._is_owner(message.author)
            manage_server_check = manage_server_auth and self._can_manage_server(message.author, message.channel)
            is_cakebot_check = (not require_non_cakebot) or (
                        require_non_cakebot and not self._is_cakebot(message.author))
            no_auth = not owner_auth and not manage_server_auth and not cakebot_perm

            perms = self._db_get_permissions(message.author.id, message.server.id)
            cakebot_perm_check = cakebot_perm and perms and cakebot_perm in perms

            if is_cakebot_check and (no_auth or owner_check or manage_server_check or cakebot_perm_check):
                await f(message)
            else:
                await self.say(message.channel, 'You\'re not allowed to do that!')

        return ret_fun

    def _db_get_permissions(self, user_id, server_id):
        self.c.execute("SELECT permissions FROM permissions WHERE user_id = ? AND server_id = ?", (user_id, server_id))
        return self.c.fetchone()

    def _db_set_permissions(self, user_id, server_id, new_perms):
        self.c.execute("INSERT INTO permissions (user_id, server_id, permissions) VALUES (?, ?, ?)",
                       (user_id, server_id, ','.join(new_perms)))

    def _db_update_permissions(self, user_id, server_id, new_perms):
        self.c.execute("UPDATE permissions SET permissions = ? WHERE user_id = ? AND server_id = ?",
                       (new_perms, user_id, server_id))

    async def _print_permissions(self, message, user):
        perms = self._db_get_permissions(user.id, message.server.id)
        if perms:
            perm_message = 'Permissions for {}: {}'.format(user, perms)
        else:
            perm_message = 'There are no set permissions for: {}'.format(user)
        if self._can_manage_server(user, message.channel):
            perm_message += '\nThis user has manage_server permissions.'

        await self.say(message.channel, perm_message)

    async def _set_permissions(self, message, user):
        async def inner(m):
            perms = self._db_get_permissions(user.id, m.server.id)
            add_perms = [comm for comm in m.content.split()[2:] if
                         comm in PermissionsModule.allowed_perm_commands]  # Filter allowed permission commands

            if add_perms:
                if perms:
                    current_perms = perms[0]
                    new_perms = current_perms + ',' + ','.join(add_perms)
                    self._db_update_permissions(user.id, m.server.id, new_perms)
                else:
                    self._db_set_permissions(user.id, m.server.id, add_perms)
                self.conn.commit()
                add_message = 'Added permissions: `{}` to {}'.format(','.join(add_perms), user)
                await self.say(m.channel, add_message)
            else:
                await self.say(m.channel, 'No permissions were added to {}!'.format(user))

        await self.auth_function(inner)(message, require_non_cakebot=True, manage_server_auth=True, owner_auth=True)

    async def permissions(self, message):
        args = message.content.split()

        # Gets permissions for mentioned user if given, otherwise defaults to calling user
        user = message.author
        if message.mentions:
            user = message.mentions[0]  # Find id of first mentioned user

        if len(args) == 1 or len(args) == 2:
            await self._print_permissions(message, user)
        elif len(args) > 2:
            await self._set_permissions(message, user)

    def _can_manage_server(self, user, channel):
        return channel.permissions_for(user).manage_server

    def _is_cakebot(self, user):
        return user.id == self.client.user.id

    def _is_owner(self, user):
        return str(user.id) == cakebot_config.OWNER_ID

    command_handlers = {
        '!permissions': permissions,
    }

    help_entries = permissions_help.help_entries
