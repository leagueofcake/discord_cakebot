from bot.types import BotABC
import random
from typing import List, Tuple
from discord.message import Message
import requests
import asyncio
import bot.cakebot_config as cakebot_config

from bot.modules.AbstractModuleInterface import AbstractModuleInterface
from bot.modules.helpers import is_integer
from bot.modules.misc import misc_help, misc_consts


def _parse_duration_str(args: List[str]) -> Tuple[int, str]:
    # Used for !timedcats. May be extended for use with other commands in the future.
    # Returns a tuple (times, duration_str)
    # Defaults to 5 m if no duration string is given
    times = 5
    duration_str = "m"

    if len(args) > 1:
        arg_times = args[1]
        if is_integer(arg_times):
            if int(arg_times) <= 60:
                times = int(arg_times)

        if len(args) > 2:
            arg_duration = args[2]
            if arg_duration in misc_consts.time_map:
                duration_str = arg_duration
    return times, duration_str


def _select_repl(char: str) -> str:
    try:
        weight = 8
        key = int(random.random() * (len(misc_consts.repl_dict[char]) + weight))
        if key < weight + 1:
            return misc_consts.repl_dict[char][
                0
            ]  # Below weight, key equals 0 (key for first/default character)
        else:
            return misc_consts.repl_dict[char][key - weight]
    except KeyError:  # Return original char if char not found in dict
        return char


def _return_troll(url: str) -> str:
    prefix = ""
    if "https://" in url:
        prefix = "https://"
    elif "http://" in url:
        prefix = "http://"
    return prefix + "".join([_select_repl(x) for x in url[len(prefix) :]])


async def timed_cats(self: BotABC, message: Message) -> None:
    async def inner(m: Message) -> None:
        times, duration_str = _parse_duration_str(m.content.split())
        unit_time = misc_consts.time_map[duration_str][0]

        unit = misc_consts.time_map[duration_str][1]
        unit_plural = misc_consts.time_map[duration_str][2]

        if times == 1:
            unit_plural = unit

        await self.say(
            m.channel,
            "Sending cats every {} for {} {}!".format(unit, times, unit_plural),
        )

        for i in range(times):
            cat_url = requests.get("http://aws.random.cat/meow").json()["file"]
            await self.say(m.channel, cat_url)
            if i == times - 1:
                await self.say(m.channel, "Finished sending cats!")
                break
            await asyncio.sleep(unit_time)

    await self.auth_function(inner)(message, owner_auth=True)


async def troll_url(self: BotABC, message: Message) -> None:
    await self.say(message.channel, _return_troll(message.content.split()[1]))
    await self.delete(message)


async def invite(self: BotABC, message: Message) -> None:
    await self.say(
        message.channel,
        "Add me to your server! Click here: {}".format(
            cakebot_config.NORMAL_INVITE_LINK
        ),
    )


async def gen_google_link(self: BotABC, message: Message) -> None:
    url = "https://www.google.com/#q=" + "+".join(message.content.split()[1:])
    await self.say(message.channel, url)


class MiscModule(AbstractModuleInterface):
    command_handlers = {
        "!timedcats": timed_cats,
        "!trollurl": troll_url,
        "!invite": invite,
        "!google": gen_google_link,
    }

    help_entries = misc_help.help_entries
