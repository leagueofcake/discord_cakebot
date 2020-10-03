from asyncio import sleep as asyncio_sleep
from bot.modules.ModuleInterface import ModuleInterface
from sqlite3 import connect as sqlite3_connect
from typing import Any, Callable, Coroutine, Dict, Optional, Set, Type, TypeVar, Union

from discord import Client
from discord.message import Message
from discord.channel import TextChannel, DMChannel, GroupChannel
from logging import Logger
import bot.cakebot_config as cakebot_config

from bot.modules.core.Core import Core
from bot.modules.HelpEntry import HelpEntry
from bot.modules.messages.MessagesModule import MessagesModule
from bot.modules.misc.MiscModule import MiscModule
from bot.modules.modtools.ModToolsModule import ModToolsModule
from bot.modules.music.MusicModule import MusicModule
from bot.modules.permissions.PermissionsModule import PermissionsModule
from bot.types import AuthInnerFunction, AuthedFunction, CommandHandler


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

    def plug_in_module(self: B, module_name: str) -> B:
        modules = {
            "core": Core,
            "misc": MiscModule,
            "music": MusicModule,
            "permissions": PermissionsModule,
            "modtools": ModToolsModule,
        }
        new_abstract_modules = {
            "messages": MessagesModule,
        }

        if module_name in modules:
            self._extend_instance(modules[module_name])
            self.modules.add(module_name)
            self.logger.info("[cakebot][modules]: {} plugged in".format(module_name))
        elif module_name in new_abstract_modules:
            # Add command handlers from module
            self.command_handlers = {
                **self.command_handlers,
                **new_abstract_modules[module_name].command_handlers,
            }

            # Add command handlers from module
            self.help_entries = {
                **self.help_entries,
                **new_abstract_modules[module_name].help_entries,
            }
        else:
            self.logger.info(
                "[cakebot][modules]: unknown module {}".format(module_name)
            )
        return self

    async def say(
        self, channel: Union[TextChannel, DMChannel, GroupChannel], message: str
    ) -> Message:
        return await channel.send(message)

    async def temp_message(
        self, channel: TextChannel, message: str, time: float = 5
    ) -> None:
        tmp = await self.say(channel, message)
        await asyncio_sleep(time)
        await self.delete(tmp)

    async def delete(self, message: Message) -> None:
        await message.delete()

    async def handle_incoming_message(self, message: Message) -> None:
        args = message.content.split()
        command = args[0]

        if command in self.command_handlers:
            await self.command_handlers[command](self, message)  # type: ignore # TODO Argument 1 has incompatible type "Bot"; expected "BotABC"

    # Overwritten by PermissionsModule if loaded, otherwise defaults to this
    def auth_function(self, f: AuthInnerFunction) -> AuthedFunction:
        async def mock_inner(
            message: Message,
            owner_auth: Optional[bool] = False,
            require_non_cakebot: Optional[bool] = False,
            manage_guild_auth: Optional[bool] = False,
        ) -> None:
            await f(message)

        return mock_inner
