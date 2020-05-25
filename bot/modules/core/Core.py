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

    async def list_modules(self, message):
        summary = '\nModules loaded:\n'
        summary += '```'
        for module in sorted(self.modules):
            summary += module + '\n'

        summary += '```'
        await self.temp_message(message.channel, summary)

    async def handle_load_module(self, message):
        async def inner(m):
            args = m.content.split()
            if len(args) > 1:
                module_name = args[1]
                if module_name not in self.modules:
                    self.load_module(module_name)
                    await self.temp_message(message.channel, 'Loaded module: ' + module_name)
                else:
                    await self.temp_message(message.channel, 'Module has already been loaded!')
            else:
                await self.temp_message(message.channel, 'Please specify a module name to load.')
        await self.auth_function(inner)(message, owner_auth=True, require_non_cakebot=True)

    async def handle_unload_module(self, message):
        async def inner(m):
            args = m.content.split()
            if len(args) > 1:
                module_name = args[1]
                if module_name in self.modules:
                    self.unload_module(module_name)
                    await self.temp_message(message.channel, 'Unloaded module: ' + module_name)
                else:
                    await self.temp_message(message.channel, 'Module has not yet been loaded!')
            else:
                await self.temp_message(message.channel,
                                        'Please specify a module name to unload.')

        await self.auth_function(inner)(message, owner_auth=True, require_non_cakebot=True)

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
        '!modules': list_modules,
        '!loadmodule': handle_load_module,
        '!unloadmodule': handle_unload_module,
        '!help': help
    }

    help_entries = {
        'modules': HelpEntry('!modules', 'Lists the currently loaded modules', '!modules', 'modules'),
        'loadmodule': HelpEntry('!loadmodule', 'Load a module', '!loadmodule', 'modules'),
        'unloadmodule': HelpEntry('!unloadmodule', 'Unload a module', '!unloadmodule', 'modules'),
        'help': HelpEntry('!help', 'Displays this message', '!help', 'general')
    }
