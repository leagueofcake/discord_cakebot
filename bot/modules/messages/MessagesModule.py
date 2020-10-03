from discord.message import Message
from bot.types import BotABC
import sys

from bot.modules.AbstractModuleInterface import AbstractModuleInterface
from bot.modules.messages import messages_help


async def hello(self: BotABC, message: Message) -> None:
    await self.say(message.channel, "Hello {}!".format(message.author.mention))


async def say_in_room(self: BotABC, message: Message) -> None:
    async def inner(m: Message) -> None:
        if m.channel_mentions:
            await self.say(m.channel_mentions[0], " ".join(m.content.split()[2:]))
        else:
            await self.say(m.channel, "No room specified!")
        await self.delete(m)

    await self.auth_function(inner)(message, owner_auth=True)


async def bye(self: BotABC, message: Message) -> None:
    async def inner(m: Message) -> None:
        await self.say(m.channel, "Logging out, bye!")
        sys.exit()

    await self.auth_function(inner)(message, owner_auth=True)


async def redirect(self: BotABC, message: Message) -> None:
    room = message.channel_mentions[0]
    await self.say(room, "`{}` redirected:".format(message.author))
    await self.say(room, " ".join(message.content.split()[2:]))
    await self.delete(message)


class MessagesModule(AbstractModuleInterface):
    command_handlers = {
        "!hello": hello,
        "!bye": bye,
        "!redirect": redirect,
        "!say": say_in_room,
    }

    help_entries = messages_help.help_entries
