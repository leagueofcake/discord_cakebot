import cakebot_config

from sqlite3 import connect as sqlite3_connect
from asyncio import sleep as asyncio_sleep

from modules.HelpEntry import HelpEntry

from modules.misc.MiscModule import MiscModule
from modules.music.MusicModule import MusicModule
from modules.permissions.PermissionsModule import PermissionsModule
from modules.messages.MessagesModule import MessagesModule
from modules.modtools.ModToolsModule import ModToolsModule


class Bot:
    def __init__(self, client, logger):
        self.client = client
        self.conn = sqlite3_connect(cakebot_config.DB_PATH)
        self.c = self.conn.cursor()

        self.logger = logger
        self.modules = set()
        self.command_handlers = {}

        self.help_entries = {
            'help': HelpEntry('!help', 'Displays this message', '!help', 'general')
        }

    def _extend_instance(self, cls):
        # Apply mixin to self
        base_cls = self.__class__
        base_cls_name = self.__class__.__name__
        self.__class__ = type(base_cls_name, (base_cls, cls), {})

        # Add command handlers from module
        self.command_handlers = {**self.command_handlers, **cls.command_handlers}

        # Add command handlers from module
        self.help_entries = {**self.help_entries, **cls.help_entries}

    def plug_in_module(self, module_name):
        modules = {
            'misc': MiscModule,
            'music': MusicModule,
            'permissions': PermissionsModule,
            'messages': MessagesModule,
            'modtools': ModToolsModule
        }

        if module_name in modules:
            self._extend_instance(modules[module_name])
            self.modules.add(module_name)
            self.logger.info('[cakebot][modules]: {} plugged in'.format(module_name))
        else:
            self.logger.info('[cakebot][modules]: unknown module {}'.format(module_name))

    async def say(self, channel, message):
        return await self.client.send_message(channel, message)

    async def temp_message(self, channel, message, time=5):
        tmp = await self.say(channel, message)
        await asyncio_sleep(time)
        await self.delete(tmp)

    async def delete(self, message):
        await self.client.delete_message(message)

    def _generate_help_summary(self):
        sorted_keys = sorted(self.help_entries)
        head = '\nCommand summary. For more information do ``!help <command>`` e.g. ``!help timedcats``\n'
        summary = head
        summary += '```'
        for command in sorted_keys:
            summary += self.help_entries[command].command.ljust(14, ' ')
            summary += self.help_entries[command].short_description + '\n'
        summary += '```'

        summary += '\nFull command list can be found at https://discord-cakebot.readthedocs.io/en/latest/command_list.html'
        return summary

    async def help(self, message):
        args = message.content.split()
        if len(args) > 1:  # specific command
            command = args[1]
            try:
                await self.temp_message(message.channel, self.help_entries[command].get_entry(), time=10)
            except KeyError:
                await self.temp_message(message.channel, 'Command not found! do ``!help`` for the command list.',
                                        time=10)
        else:  # command list summary
            await self.temp_message(message.channel, self._generate_help_summary(), time=10)

    async def handle_incoming_message(self, message):
        args = message.content.split()
        command = args[0]

        if command in self.command_handlers:
            await self.command_handlers[command](self, message)
        elif command == '!help':
            await self.help(message)
