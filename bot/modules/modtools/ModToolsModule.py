from datetime import datetime
from discord import errors as discord_errors, ActivityType

from bot.modules.ModuleInterface import ModuleInterface
from bot.modules.modtools import modtools_help
from bot.modules.helpers import is_integer, get_full_username


class ModToolsModule(ModuleInterface):
    async def purge(self, message):
        async def inner(m):
            args = m.content.split()

            await self.delete(m)
            if len(args) < 2:
                await self.say(
                    m.channel, "Please specify the number of messages to purge."
                )
            else:
                if m.mentions and len(args) >= 3:
                    purge_user = m.mentions[0]  # Find id of first mentioned user
                    if not is_integer(args[2]):
                        await self.say(
                            m.channel,
                            "Please specify a valid number of messages to purge. (1-100)",
                        )
                    else:
                        num = int(args[2])
                        await self._purge_messages(
                            message=message, purge_user=purge_user, num=num
                        )
                else:
                    if not is_integer(args[1]):
                        await self.say(
                            m.channel,
                            "Please specify a valid number of messages to purge. (1-100)",
                        )
                    else:
                        num = int(args[1])
                        try:
                            deleted = await m.channel.purge(limit=num)
                            await self.temp_message(
                                m.channel, "Purged {} messages.".format(len(deleted))
                            )
                        except discord_errors.HTTPException:  # Delete individually
                            async for log in m.channel.history(limit=num):
                                await self.delete(log)

        await self.auth_function(inner)(
            message, manage_guild_auth=True, require_non_cakebot=True
        )

    async def del_user_messages(self, message):
        async def inner(m):
            args = m.content.split()
            if len(args) == 1 or (
                len(args) == 2 and is_integer(args[1]) and args[1] == "1"
            ):
                await self.delete(m)
                async for log in m.channel.history(limit=500):
                    if log.author.id == m.author.id:
                        await self.delete(log)
                        break
            elif len(args) == 2:
                await self.delete(m)
                purge_user_id = m.author
                if not is_integer(args[1]):
                    await self.say(
                        m.channel,
                        "Please specify a valid number of messages to delete. (1-100)",
                    )
                else:
                    num = int(args[1])
                    await self._purge_messages(
                        message=m, purge_user=purge_user_id, num=num
                    )

        await self.auth_function(inner)(message, require_non_cakebot=True)

    async def _print_log_channel(self, message):
        log_channel = self.client.get_channel(
            self._get_log_channel_id(message.guild.id)
        )
        if log_channel:
            await self.temp_message(
                message.channel, "Log channel is: {}".format(log_channel.mention)
            )
        else:
            await self.temp_message(
                message.channel,
                "No log channel configured! Add one with `!logchannel set`",
            )

    async def _set_log_channel(self, message):
        async def inner(m):
            log_channel = self.client.get_channel(self._get_log_channel_id(m.guild.id))
            if log_channel:
                self._update_log_channel(m.guild.id, m.channel.id)
            else:
                self._add_log_channel(m.guild.id, m.channel.id)
            await self.say(
                m.channel, "Set {} as the log channel!".format(m.channel.mention)
            )
            self.conn.commit()

        await self.auth_function(inner)(
            message,
            manage_guild_auth=True,
            cakebot_perm="logchannel",
            require_non_cakebot=True,
        )

    async def log_channel(self, message):
        args = message.content.split()
        if len(args) == 1:
            await self._print_log_channel(message)
        else:
            if len(args) == 2 and args[1] == "set":
                await self._set_log_channel(message)

    async def handle_guild_channel_update(self, before, after):
        log_channel = self.client.get_channel(self._get_log_channel_id(before.guild.id))

        if log_channel:
            local_message_time = datetime.now().strftime("%H:%M:%S")

            channel_mention = before.mention
            if before.name != after.name:
                message = (
                    "[{}] {} *changed channel name*\n"
                    "Before: {}\n"
                    "After+: {}".format(
                        local_message_time, channel_mention, before.name, after.name
                    )
                )
                await self.say(log_channel, message)

            if hasattr(before, "topic") and before.topic != after.topic:
                message = (
                    "[{}] {} *changed topic contents*\n"
                    "Before: {}\n"
                    "After+: {}".format(
                        local_message_time, channel_mention, before.topic, after.topic
                    )
                )
                await self.say(log_channel, message)

    async def handle_edited_message(self, before, after):
        log_channel = self.client.get_channel(self._get_log_channel_id(before.guild.id))
        if log_channel and before.content != after.content:
            await self.say(
                log_channel, ModToolsModule._gen_edit_message_log(before, after)
            )

    async def handle_deleted_message(self, message):
        log_channel = self.client.get_channel(
            self._get_log_channel_id(message.guild.id)
        )

        if log_channel:
            await self.say(log_channel, ModToolsModule._gen_delete_message_log(message))

    async def handle_member_update(self, before, after):
        log_channel = self.client.get_channel(self._get_log_channel_id(before.guild.id))

        if log_channel:
            local_message_time = datetime.now().strftime("%H:%M:%S")
            before_roles = ", ".join(
                [role.name for role in before.roles if role.name != "@everyone"]
            )
            after_roles = ", ".join(
                [role.name for role in after.roles if role.name != "@everyone"]
            )

            if before.nick != after.nick:
                message = (
                    "[{}] {} *changed nickname*\n"
                    "Before: {}\n"
                    "After+: {}".format(
                        local_message_time,
                        get_full_username(before),
                        before.display_name,
                        after.display_name,
                    )
                )
                await self.say(log_channel, message)

            elif before_roles != after_roles:
                message = (
                    "[{}] {} *changed roles*\n"
                    "Before: {}\n"
                    "After+: {}".format(
                        local_message_time,
                        get_full_username(before),
                        before_roles,
                        after_roles,
                    )
                )
                await self.say(log_channel, message)

        # TODO UPDATE FOR discord.py 1.0+
        """
        before_activities = [a for a in before.activities if a.type == ActivityType.playing]
        after_activities = [a for a in after.activities if a.type == ActivityType.playing]
        if before_activities != after_activities:
            await self._auto_rename_voice_channel(after, before, after)
        """

    async def _auto_rename_voice_channel(self, before, after):
        # TODO UPDATE FOR discord.py 1.0+
        pass
        """
        if member.guild.id in (139345703800406016, 178312027041824768):  # Only use on main/dev server
            default_list = ["Gaming Channel 1", "Gaming Channel 2", "Gaming Channel 3", "Music Channel"]

            if after.channel:
                game_count = {}

                for member in after.channel.members:
                    member_activities = [a for a in member.activities if a.type == ActivityType.playing]
                    if member_activities:
                        if member_activities[0].name not in game_count:
                            game_count[member_activities[0].name] = 1
                        else:
                            game_count[member_activities[0].name] += 1
                if game_count:
                    # Select game with highest current players
                    new_channel_names = [key for m in [max(game_count.values())] for key, val in game_count.items() if
                                         val == m]
                    for new_channel_name in new_channel_names:
                        if new_channel_name:  # Non-blank new channel name, set as new channel name
                            await before.channel.edit(name=new_channel_name)
                            break
                else:
                    default_name = default_list[after.channel.position]
                    await after.channel.edit(name=default_name)

                if before.channel:
                    if len(before.channel.members) == 0:  # No more members, reset to default name
                        default_name = default_list[before.channel.position]
                        await before.channel.edit(name=default_name)

            # If voice channel being left has no more members, reset to default name
            if before.channel:
                if len(before.channel.members) == 0:
                    default_name = default_list[before.channel.position]
                    await before.channel.edit(name=default_name)
        """

    async def handle_voice_channel_update(self, member, before, after):
        await self._auto_rename_voice_channel(member, before, after)

    def _get_log_channel_id(self, server_id):
        self.c.execute(
            "SELECT channel_id FROM log_channel WHERE server_id = ?", (server_id,)
        )
        res = self.c.fetchone()
        if res:
            return int(res[0])
        return None

    def _add_log_channel(self, server_id, channel_id):
        self.c.execute(
            "INSERT INTO log_channel(server_id, channel_id) VALUES (?, ?)",
            (server_id, channel_id),
        )

    def _update_log_channel(self, server_id, channel_id):
        self.c.execute(
            "UPDATE log_channel SET channel_id = ? WHERE server_id = ?",
            (channel_id, server_id),
        )

    @staticmethod
    def _gen_edit_message_log(before, after):
        before_content = before.clean_content
        after_content = after.clean_content
        local_message_time = datetime.now().strftime("%H:%M:%S")

        if before.attachments:
            before_content += " " + before.attachments[0]["proxy_url"]
        if after.attachments:
            after_content += " " + after.attachments[0]["proxy_url"]

        log_message = (
            "[{}] {} *edited their message in* {}\n"
            "Before: {}\n"
            "After+: {}".format(
                local_message_time,
                get_full_username(before.author),
                before.channel.mention,
                before_content,
                after_content,
            )
        )
        return log_message

    @staticmethod
    def _gen_delete_message_log(message):
        clean_content = message.clean_content
        local_message_time = datetime.now().strftime("%H:%M:%S")
        username = get_full_username(message.author)

        if message.attachments:
            clean_content += " " + message.attachments[0]["proxy_url"]

        return "[{}] {} *deleted their message in* {}\n" "{}".format(
            local_message_time, username, message.channel.mention, clean_content
        )

    async def _purge_messages(self, message, purge_user, num):
        if 1 <= num <= 100:
            to_delete = []
            async for log in message.channel.history(limit=500):
                if log.author.id == purge_user.id:
                    to_delete.append(log)
                if len(to_delete) == num:  # Found num amount of messages
                    break

            if len(to_delete) == 1:
                await to_delete[0].delete()
            else:
                await message.channel.delete_messages(to_delete)
            await self.temp_message(
                message.channel,
                "Purged {} messages from {}.".format(len(to_delete), purge_user),
            )
        else:
            await self.temp_message(
                message.channel,
                "Please specify a valid number of messages to purge. (1-100)",
            )

    command_handlers = {
        "!logchannel": log_channel,
        "!purge": purge,
        "!del": del_user_messages,
    }

    help_entries = modtools_help.help_entries
