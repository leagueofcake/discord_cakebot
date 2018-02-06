from asyncio import sleep as asyncio_sleep
from modules.ModuleInterface import ModuleInterface
from modules.HelpEntry import HelpEntry


class Core(ModuleInterface):
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

    command_handlers = {
        '!help': help
    }

    help_entries = {
        'help': HelpEntry('!help', 'Displays this message', '!help', 'general')
    }
