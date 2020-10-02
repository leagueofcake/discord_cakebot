from typing import Callable
from discord.message import Message

CommandHandler = Callable[[Message], None]
