from abc import ABC, abstractmethod
from bot.modules.HelpEntry import HelpEntry
from bot.types import BotABC
from typing import Dict
from bot.types import CommandHandler

"""
TODO: migrate all modules off ModuleInterface
Each command handler should now have the self parameter be annotated as a Bot, so we don't need
the mock __init__ to describe all the available attributes on the class.

Need to think of a way to handle mixins/method overriding. I think the way forward is to make the
handle_x methods also (internal) command handler instances.
"""


class AbstractModuleInterface(ABC):
    command_handlers: Dict[str, CommandHandler]
    help_entries: Dict[str, HelpEntry]
