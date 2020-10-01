from bot.modules.ModuleInterface import ModuleInterface
from sqlite3 import connect as sqlite3_connect
from typing import Dict, Set, Type, TypeVar, Union

from discord import Client
from logging import Logger
import bot.cakebot_config as cakebot_config

from bot.modules.core.Core import Core
from bot.modules.HelpEntry import HelpEntry
from bot.modules.messages.MessagesModule import MessagesModule
from bot.modules.misc.MiscModule import MiscModule
from bot.modules.modtools.ModToolsModule import ModToolsModule
from bot.modules.music.MusicModule import MusicModule
from bot.modules.permissions.PermissionsModule import PermissionsModule
from bot.types import CommandHandler


B = TypeVar("B", bound="Bot")


class Bot:
    def __init__(self, client: Client, logger: Logger) -> None:
        self.client = client
        self.conn = sqlite3_connect(cakebot_config.DB_PATH)
        self.c = self.conn.cursor()

        self.logger = logger
        self.modules: Set[str] = set()
        self.command_handlers: Dict[str, CommandHandler] = {}

        self.help_entries: Dict[str, HelpEntry] = {}

    def _extend_instance(self, cls: Union[Type[B], Type[ModuleInterface]]) -> None:
        # Apply mixin to self
        base_cls = self.__class__
        base_cls_name = self.__class__.__name__
        self.__class__ = type(
            base_cls_name, (cls, base_cls), {}
        )  # cls overrides methods of base_cls

        # Add command handlers from module
        self.command_handlers = {**self.command_handlers, **cls.command_handlers}

        # Add command handlers from module
        self.help_entries = {**self.help_entries, **cls.help_entries}

    def plug_in_module(self, module_name: str) -> None:
        modules = {
            "core": Core,
            "misc": MiscModule,
            "music": MusicModule,
            "permissions": PermissionsModule,
            "messages": MessagesModule,
            "modtools": ModToolsModule,
        }

        if module_name in modules:
            self._extend_instance(modules[module_name])
            self.modules.add(module_name)
            self.logger.info("[cakebot][modules]: {} plugged in".format(module_name))
        else:
            self.logger.info(
                "[cakebot][modules]: unknown module {}".format(module_name)
            )

    async def handle_incoming_message(self, message):
        args = message.content.split()
        command = args[0]

        if command in self.command_handlers:
            await self.command_handlers[command](self, message)

    async def handle_edited_message(
        self, before, after
    ):  # Overriden by modtools module
        pass

    async def handle_deleted_message(self, message):  # Overriden by modtools module
        pass

    async def handle_guild_channel_update(
        self, before, after
    ):  # Overriden by modtools module
        pass

    async def handle_member_update(self, before, after):  # Overriden by modtools module
        pass

    async def handle_voice_channel_update(
        self, member, before, after
    ):  # Overriden by modtools module
        pass
