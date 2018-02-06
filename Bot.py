import asyncio
import sqlite3

from discord import errors as discord_errors

import cakebot_help
from datetime import datetime
import cakebot_config
from modules.helpers import is_integer, get_full_username
from modules.modtools import add_log_channel, update_log_channel, get_log_channel_id, gen_edit_message_log, \
    gen_delete_message_log, purge_messages

from modules.MiscModule import MiscModule
from modules.MusicModule import MusicModule
from modules.PermissionsModule import PermissionsModule
from modules.MessagesModule import MessagesModule


class Bot:
    def __init__(self, client, logger):
        self.client = client
        self.conn = sqlite3.connect(cakebot_config.DB_PATH)
        self.c = self.conn.cursor()

        self.logger = logger
        self.modules = {}

    def _extend_instance(self, cls):
        # Apply mixin to self
        base_cls = self.__class__
        base_cls_name = self.__class__.__name__
        self.__class__ = type(base_cls_name, (base_cls, cls), {})

    def plug_in_module(self, module_name):
        allowed_modules = ['misc', 'music', 'permissions', 'messages']
        if module_name in allowed_modules:
            if module_name == 'misc':
                self._extend_instance(MiscModule)
            elif module_name == 'music':
                self._extend_instance(MusicModule)
            elif module_name == 'permissions':
                self._extend_instance(PermissionsModule)
            elif module_name == 'messages':
                self._extend_instance(MessagesModule)
            self.logger.info('[cakebot]: module {} plugged in'.format(module_name))

    async def say(self, channel, message):
        return await self.client.send_message(channel, message)

    async def temp_message(self, channel, message, time=5):
        tmp = await self.say(channel, message)
        await asyncio.sleep(time)
        await self.delete(tmp)

    async def delete(self, message):
        await self.client.delete_message(message)

    async def purge(self, message):
        async def inner(m):
            args = m.content.split()

            await self.delete(m)
            if len(args) < 2:
                await self.say(m.channel, "Please specify the number of messages to purge.")
            else:
                if m.mentions and len(args) >= 3:
                    purge_user = m.mentions[0]  # Find id of first mentioned user
                    if not is_integer(args[2]):
                        await self.say(m.channel, "Please specify a valid number of messages to purge. (1-100)")
                    else:
                        num = int(args[2])
                        await purge_messages(message=message, client=self.client, purge_user=purge_user, num=num)
                else:
                    if not is_integer(args[1]):
                        await self.say(m.channel, "Please specify a valid number of messages to purge. (1-100)")
                    else:
                        num = int(args[1])
                        try:
                            deleted = await self.client.purge_from(m.channel, limit=num)
                            await self.temp_message(m.channel, "Purged {} messages.".format(len(deleted)))
                        except discord_errors.HTTPException:  # Delete individually
                            async for log in self.client.logs_from(m.channel, limit=num):
                                await self.delete(log)

        await self.auth_function(inner)(message, manage_server_auth=True, require_non_cakebot=True)

    async def del_user_messages(self, message):
        async def inner(m):
            args = m.content.split()
            if len(args) == 1 or (len(args) == 2 and is_integer(args[1]) and args[1] == '1'):
                await self.delete(m)
                async for log in self.client.logs_from(m.channel, limit=500):
                    if log.author.id == m.author.id:
                        await self.delete(log)
                        break
            elif len(args) == 2:
                await self.delete(m)
                purge_user_id = m.author
                if not is_integer(args[1]):
                    await self.say(m.channel, "Please specify a valid number of messages to delete. (1-100)")
                else:
                    num = int(args[1])
                    await purge_messages(message=m, client=self.client, purge_user=purge_user_id, num=num)
        await self.auth_function(inner)(message, require_non_cakebot=True)

    async def _print_log_channel(self, message):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, message.server.id))
        if log_channel:
            await self.temp_message(message.channel, 'Log channel is: {}'.format(log_channel.mention))
        else:
            await self.temp_message(message.channel, 'No log channel configured! Add one with `!logchannel set`')

    async def _set_log_channel(self, message):
        async def inner(m):
            log_channel = self.client.get_channel(get_log_channel_id(self.c, m.server.id))
            if log_channel:
                update_log_channel(self.c, m.server.id, m.channel.id)
            else:
                add_log_channel(self.c, m.server.id, m.channel.id)
            await self.say(m.channel, 'Set {} as the log channel!'.format(m.channel.mention))
            self.conn.commit()
        await self.auth_function(inner)(message, manage_server_auth=True, cakebot_perm='logchannel', require_non_cakebot=True)

    async def log_channel(self, message):
        args = message.content.split()
        if len(args) == 1:
            await self._print_log_channel(message)
        else:
            if len(args) == 2 and args[1] == 'set':
                await self._set_log_channel(message)

    async def help(self, message):
        args = message.content.split()
        if len(args) > 1:  # specific command
            command = args[1]
            try:
                await self.temp_message(message.channel, cakebot_help.get_entry(command), time=10)
            except KeyError:
                await self.temp_message(message.channel, 'Command not found! do ``!help`` for the command list.', time=10)
        else:  # command list summary
            await self.temp_message(message.channel, cakebot_help.generate_summary(), time=10)

    async def handle_channel_update(self, before, after):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, before.server.id))

        if log_channel:
            local_message_time = datetime.now().strftime("%H:%M:%S")

            channel_mention = before.mention
            if before.name != after.name:
                message = '[{}] {} *changed channel name*\n' \
                          'Before: {}\n' \
                          'After+: {}'.format(local_message_time, channel_mention, before.name, after.name)
                await self.say(log_channel, message)
            if before.topic != after.topic:
                message = '[{}] {} *changed topic contents*\n' \
                          'Before: {}\n' \
                          'After+: {}'.format(local_message_time, channel_mention, before.topic, after.topic)
                await self.say(log_channel, message)

    async def handle_edited_message(self, before, after):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, before.server.id))
        if log_channel and before.content != after.content:
            await self.say(log_channel, gen_edit_message_log(before, after))

    async def handle_deleted_message(self, message):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, message.server.id))

        if log_channel:
            await self.say(log_channel, gen_delete_message_log(message))

    async def handle_member_update(self, before, after):
        log_channel = self.client.get_channel(get_log_channel_id(self.c, before.server.id))

        if log_channel:
            local_message_time = datetime.now().strftime("%H:%M:%S")
            before_roles = ", ".join([role.name for role in before.roles if role.name != "@everyone"])
            after_roles = ", ".join([role.name for role in after.roles if role.name != "@everyone"])

            if before.nick != after.nick:
                message = '[{}] {} *changed nickname*\n' \
                          'Before: {}\n' \
                          'After+: {}'.format(local_message_time, get_full_username(before),
                                              before.display_name,
                                              after.display_name)
                await self.say(log_channel, message)

            elif before_roles != after_roles:
                message = '[{}] {} *changed roles*\n' \
                          'Before: {}\n' \
                          'After+: {}'.format(local_message_time, get_full_username(before),
                                              before_roles,
                                              after_roles)
                await self.say(log_channel, message)

        if before.game != after.game:
            await self._auto_rename_voice_channel(before, after)

    async def _auto_rename_voice_channel(self, before, after):
        if before.server.id in ("139345703800406016", "178312027041824768"):  # Only use on main/dev server
            default_list = ["Gaming Channel 1", "Gaming Channel 2", "Gaming Channel 3", "Music Channel"]

            if after.voice_channel:
                game_count = {}
                voice_members = after.voice_channel.voice_members

                for member in voice_members:
                    if member.game:
                        if member.game.name not in game_count:
                            game_count[member.game.name] = 1
                        else:
                            game_count[member.game.name] += 1
                if game_count:
                    # Select game with highest current players
                    new_channel_names = [key for m in [max(game_count.values())] for key,val in game_count.items() if val == m]
                    for new_channel_name in new_channel_names:
                        if new_channel_name:  # Non-blank new channel name, set as new channel name
                            await self.client.edit_channel(after.voice_channel, name=new_channel_name)
                            break
                else:
                    default_name = default_list[after.voice_channel.position]
                    await self.client.edit_channel(after.voice_channel, name=default_name)

                if before.voice_channel:
                    if len(before.voice_channel.voice_members) == 0:  # No more members, reset to default name
                        default_name = default_list[before.voice_channel.position]
                        await self.client.edit_channel(before.voice_channel, name=default_name)

            # If voice channel being left has no more members, reset to default name
            if before.voice_channel:
                if len(before.voice_channel.voice_members) == 0:
                    default_name = default_list[before.voice_channel.position]
                    await self.client.edit_channel(before.voice_channel, name=default_name)

    async def handle_voice_channel_update(self, before, after):
        await self._auto_rename_voice_channel(before, after)

