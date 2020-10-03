from abc import ABC
from typing import Any, Callable, Coroutine, Optional, Protocol, Union
from discord.message import Message
from discord.channel import TextChannel, DMChannel, GroupChannel


AuthInnerFunction = Callable[[Message], Coroutine[Any, Any, None]]


class AuthedFunction(Protocol):
    def __call__(
        self,
        message: Message,
        owner_auth: Optional[bool] = False,
        require_non_cakebot: Optional[bool] = False,
        manage_guild_auth: Optional[bool] = False,
    ) -> Coroutine[Any, Any, None]:
        ...


class BotABC(ABC):
    async def say(
        self, channel: Union[TextChannel, DMChannel, GroupChannel], message: str
    ) -> Message:
        ...

    async def temp_message(
        self, channel: TextChannel, message: str, time: float = 5
    ) -> None:
        ...

    async def delete(self, message: Message) -> None:
        ...

    def auth_function(self, f: AuthInnerFunction) -> AuthedFunction:
        ...

    async def handle_edited_message(
        self, before, after
    ):  # Overriden by modtools module
        ...

    async def handle_deleted_message(self, message):  # Overriden by modtools module
        ...

    async def handle_guild_channel_update(
        self, before, after
    ):  # Overriden by modtools module
        ...

    async def handle_member_update(self, before, after):  # Overriden by modtools module
        ...

    async def handle_voice_channel_update(
        self, member, before, after
    ):  # Overriden by modtools module
        ...


CommandHandler = Callable[[BotABC, Message], Coroutine[Any, Any, None]]
