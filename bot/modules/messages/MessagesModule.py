import sys

from modules.ModuleInterface import ModuleInterface
from modules.messages import messages_help


class MessagesModule(ModuleInterface):
    async def hello(self, message):
        await self.say(message.channel, 'Hello {}!'.format(message.author.mention))

    async def say_in_room(self, message):
        async def inner(m):
            if m.channel_mentions:
                await self.say(m.channel_mentions[0], ' '.join(m.content.split()[2:]))
            else:
                await self.say(m.channel, 'No room specified!')
            await self.delete(m)

        await self.auth_function(inner)(message, owner_auth=True)

    async def bye(self, message):
        async def inner(m):
            await self.say(m.channel, 'Logging out, bye!')
            sys.exit()

        await self.auth_function(inner)(message, owner_auth=True)

    async def redirect(self, message):
        room = message.channel_mentions[0]
        await self.say(room, '`{}` redirected:'.format(message.author))
        await self.say(room, ' '.join(message.content.split()[2:]))
        await self.delete(message)

    command_handlers = {
        '!hello': hello,
        '!bye': bye,
        '!redirect': redirect,
        '!say': say_in_room,
    }

    help_entries = messages_help.help_entries