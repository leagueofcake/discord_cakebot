import asyncio
import sqlite3

import cakebot_help
import cakebot_config

from modules.MiscModule import MiscModule
from modules.MusicModule import MusicModule
from modules.PermissionsModule import PermissionsModule
from modules.MessagesModule import MessagesModule
from modules.ModToolsModule import ModToolsModule


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
        allowed_modules = ['misc', 'music', 'permissions', 'messages', 'modtools']
        if module_name in allowed_modules:
            if module_name == 'misc':
                self._extend_instance(MiscModule)
            elif module_name == 'music':
                self._extend_instance(MusicModule)
            elif module_name == 'permissions':
                self._extend_instance(PermissionsModule)
            elif module_name == 'messages':
                self._extend_instance(MessagesModule)
            elif module_name == 'modtools':
                self._extend_instance(ModToolsModule)
            self.logger.info('[cakebot]: module {} plugged in'.format(module_name))

    async def say(self, channel, message):
        return await self.client.send_message(channel, message)

    async def temp_message(self, channel, message, time=5):
        tmp = await self.say(channel, message)
        await asyncio.sleep(time)
        await self.delete(tmp)

    async def delete(self, message):
        await self.client.delete_message(message)

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
