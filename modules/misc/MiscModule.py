import random
import requests
import asyncio

import cakebot_config
from modules.helpers import is_integer
from modules.ModuleInterface import ModuleInterface
from modules.misc.repl_dict import repl_dict

class MiscModule(ModuleInterface):
    async def timed_cats(self, message):
        async def inner(m):
            times, duration_str = MiscModule._parse_duration_str(m.content.split())
            unit_time = cakebot_config.time_map[duration_str][0]

            unit = cakebot_config.time_map[duration_str][1]
            unit_plural = cakebot_config.time_map[duration_str][2]

            if times == 1:
                unit_plural = unit

            await self.say(m.channel, 'Sending cats every {} for {} {}!'.format(unit, times, unit_plural))

            for i in range(times):
                cat_url = requests.get('http://random.cat/meow').json()['file']
                await self.say(m.channel, cat_url)
                if i == times - 1:
                    await self.say(m.channel, 'Finished sending cats!')
                    break
                await asyncio.sleep(unit_time)

        await self.auth_function(inner)(message, owner_auth=True)

    async def troll_url(self, message):
        await self.say(message.channel, MiscModule._return_troll(message.content.split()[1]))
        await self.delete(message)

    async def invite(self, message):
        await self.say(message.channel,
                       'Add me to your server! Click here: {}'.format(cakebot_config.NORMAL_INVITE_LINK))

    async def gen_google_link(self, message):
        url = 'https://www.google.com/#q=' + '+'.join(message.content.split()[1:])
        await self.say(message.channel, url)

    @staticmethod
    def _parse_duration_str(args):
        # Used for !timedcats. May be extended for use with other commands in the future.
        # Returns a tuple (times, duration_str)
        # Defaults to 5 m if no duration string is given
        times = 5
        duration_str = 'm'

        if len(args) > 1:
            arg_times = args[1]
            if is_integer(arg_times):
                if int(arg_times) <= 60:
                    times = int(arg_times)

            if len(args) > 2:
                arg_duration = args[2]
                if arg_duration in cakebot_config.time_map:
                    duration_str = arg_duration
        return times, duration_str

    @staticmethod
    def _select_repl(char):
        try:
            weight = 8
            key = int(random.random() * (len(repl_dict[char]) + weight))
            if key < weight + 1:
                return repl_dict[char][0]  # Below weight, key equals 0 (key for first/default character)
            else:
                return repl_dict[char][key - weight]
        except KeyError:  # Return original char if char not found in dict
            return char

    @staticmethod
    def _return_troll(url):
        prefix = ''
        if 'https://' in url:
            prefix = 'https://'
        elif 'http://' in url:
            prefix = 'http://'
        return prefix + ''.join([MiscModule._select_repl(x) for x in url[len(prefix):]])

    command_handlers = {
        '!timedcats': timed_cats,
        '!trollurl': troll_url,
        '!invite': invite,
        '!google': gen_google_link
    }
