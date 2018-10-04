Developing Modules
==================

Custom modules are all built off the ModuleInterface, which specifies two main things:

1. Common state that must be provided by your module to function properly (e.g. ``command_handlers`` and ``help_entries``), and;
2. Methods that each module is provided access to (e.g. ``say()`` and ``auth_function()``).

``command_handlers`` provides a mapping between a command said to cakebot in Discord, and a function which handles the command.
For example, in the sample module below, the command ``!foo`` is mapped to the asynchronous function ``foo()``.

Sample Custom Module
--------------------
Here we define a simple custom module with a single command: ``!foo``, along with its corresponding help entry file.

In ``mymodule_help.py``: ::

    from modules.HelpEntry import HelpEntry

    _foo_desc = 'cakebot says foo! '
    _foo_usage = '!foo'

    help_entries = {
        'foo':        HelpEntry('!foo', _foo_desc, _foo_usage, 'miscellaneous')
    }


In ``MyModule.py``: ::

    from modules.ModuleInterface import ModuleInterface

    class MyModule(ModuleInterface):
        async def foo(self, message):
            await self.say(message.channel, "Foo")

        command_handlers = {
            "!foo": foo
        }

        help_entries = mymodule_help.help_entries

Loading Custom Modules into cakebot
-----------------------------------

1. Add the import for your module into ``Bot.py``
2. Add the module into Bot._modules, with a name to identify it for loading. Note this identifier cannot be a duplicate of any existing identifiers.
3. Load the module in ``run.py`` using ``bot.load_module(identifier)``, with the identifier you chose above.

In ``Bot.py``: ::

    from modules.core.Core import Core
    # Other module imports...
    from modules.mymodule.MyModule import MyModule

    class Bot:
        _modules = {
            'core': Core,
            # Other modules...
            'mymodule': MyModule
        }

In ``run.py``: ::

    bot = Bot(client, logger)
    bot.load_module('core')
    # Other module loaders...
    bot.load_module('mymodule')

