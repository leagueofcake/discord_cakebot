import random
import requests
import asyncio
from .helpers import is_integer
import cakebot_config
from modules.ModuleInterface import ModuleInterface


class MiscModule(ModuleInterface):
    repl_dict = {'!': ('!', 'ǃ', '！'),
                 '"': ('"', '״', '″', '＂'),
                 '$': ('$', '＄'),
                 '%': ('%', '％'),
                 '&': ('&', '＆'),
                 "'": ("'", "＇"),
                 '(': ('(', '﹝', '（',),
                 ')': (')', '﹞', '）'),
                 '*': ('*', '⁎', '＊'),
                 '+': ('+', '＋'),
                 ',': (',', '‚', '，'),
                 '-': ('-', '‐', '－'),
                 #'.': ('.', '٠', '۔', '܁', '܂', '․', '‧', '。', '．', '｡'),
                 '/': ('/', '̸', '⁄', '∕', '╱', '⫻', '⫽', '／', 'ﾉ'),
                 '0': ('0', 'O', 'o', 'Ο', 'ο', 'О', 'о', 'Օ', 'Ｏ', 'ｏ'),
                 '1': ('1', 'I', 'ا', '１'),
                 '1': ('1', 'I', 'ا', '１'),
                 '2': ('2', '２'),
                 '3': ('3', '３'),
                 '4': ('4', '４'),
                 '5': ('5', '５'),
                 '6': ('6', '６'),
                 '7': ('7', '７'),
                 '8': ('8', 'Ց', '８'),
                 '9': ('9', '９'),
                 ':': (':', '։', '܃', '܄', '∶', '꞉', '：'),
                 ';': (';', ';', '；'),
                 '<': ('<', '‹', '＜'),
                 '=': ('=', '＝'),
                 '>': ('>', '›', '＞'),
                 '?': ('?', '？'),
                 '@': ('@', '＠'),
                 '[': ('[', '［'),
                 '\\': ('\\', '＼'),
                 ']': (']', '］'),
                 '^': ('^', '＾'),
                 '_': ('_', '＿'),
                 '`': ('`', '｀'),
                 'a': ('a', 'A', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'à', 'á', 'â', 'ã', 'ä', 'å', 'ɑ', 'Α', 'α', 'а', 'Ꭺ', 'Ａ', 'ａ'),
                 'b': ('b', 'B', 'ß', 'ʙ', 'Β', 'β', 'В', 'Ь', 'Ᏼ', 'ᛒ', 'Ｂ', 'ｂ'),
                 'c': ('c', 'C', 'ϲ', 'Ϲ', 'С', 'с', 'Ꮯ', 'Ⅽ', 'ⅽ', 'Ｃ', 'ｃ'),
                 'd': ('d', 'D', 'Ď', 'ď', 'Đ', 'đ', 'ԁ', 'ժ', 'Ꭰ', 'Ⅾ', 'ⅾ', 'Ｄ', 'ｄ'),
                 'e': ('e', 'E', 'È', 'É', 'Ê', 'Ë', 'é', 'ê', 'ë', 'Ē', 'ē', 'Ĕ', 'ĕ', 'Ė', 'ė', 'Ę', 'Ě', 'ě', 'Ε', 'Е', 'е', 'Ꭼ', 'Ｅ', 'ｅ'),
                 'f': ('f', 'F', 'Ϝ', 'Ｆ', 'ｆ'),
                 'g': ('g', 'G', 'ɡ', 'ɢ', 'Ԍ', 'ն', 'Ꮐ', 'Ｇ', 'ｇ'),
                 'h': ('h', 'H', 'ʜ', 'Η', 'Н', 'һ', 'Ꮋ', 'Ｈ', 'ｈ'),
                 'i': ('i', 'I', 'l', 'ɩ', 'Ι', 'І', 'і', 'ᛁ', 'ا', 'Ꭵ', 'Ⅰ', 'ⅰＩ', 'ｉ'),
                 'j': ('j', 'J', 'ϳ', 'Ј', 'ј', 'յ', 'Ꭻ', 'Ｊ', 'ｊ'),
                 'k': ('k', 'K', 'Κ', 'κ', 'К', 'Ꮶ', 'ᛕ', 'K', 'Ｋ', 'ｋ'),
                 'l': ('l', 'L', 'ʟ', 'ι', 'ا', 'Ꮮ', 'Ⅼ', 'ⅼ', 'Ｌ', 'ｌ'),
                 'm': ('m', 'M', 'Μ', 'Ϻ', 'М', 'Ꮇ', 'ᛖ', 'Ⅿ', 'ⅿ', 'Ｍ', 'ｍ'),
                 'n': ('n', 'N', 'ɴ', 'Ν', 'Ｎ', 'ｎ'),
                 'o': ('o', '0', 'O', 'o', 'Ο', 'ο', 'О', 'о', 'Օ', 'Ｏ', 'ｏ'),
                 'p': ('p', 'P', 'Ρ', 'ρ', 'Р', 'р', 'Ꮲ', 'Ｐ', 'ｐ'),
                 'q': ('q', 'Q', 'Ⴍ', 'Ⴓ', 'Ｑ', 'ｑ'),
                 'r': ('r', 'R', 'ʀ', 'Ի', 'Ꮢ', 'ᚱ', 'Ｒ', 'ｒ'),
                 's': ('s', 'S', 'Ѕ', 'ѕ', 'Տ', 'Ⴝ', 'Ꮪ', 'Ｓ', 'ｓ'),
                 't': ('t', 'T', 'Τ', 'τ', 'Т', 'Ꭲ', 'Ｔ', 'ｔ'),
                 'u': ('u', 'U', 'μ', 'υ', 'Ա', 'Ս', '⋃', 'Ｕ', 'ｕ'),
                 'v': ('v', 'V', 'ν', 'Ѵ', 'ѵ', 'Ꮩ', 'Ⅴ', 'ⅴ', 'Ｖ', 'ｖ'),
                 'w': ('w', 'W', 'ѡ', 'Ꮃ', 'Ｗ', 'ｗ'),
                 'x': ('x', 'X', 'Χ', 'χ', 'Х', 'х', 'Ⅹ', 'ⅹ', 'Ｘ', 'ｘ'),
                 'y': ('y', 'Y', 'ʏ', 'Υ', 'γ', 'у', 'Ү', 'Ｙ', 'ｙ'),
                 'z': ('z', 'Z', 'Ζ', 'Ꮓ', 'Ｚ', 'ｚ'),
                 '{': ('{', '｛'),
                 '|': ('|', 'ǀ', 'ا', '｜'),
                 '}': ('}', '｝'),
                 '~': ('~', '⁓', '～'),
                 }

    def _select_repl(self, char):
        try:
            weight = 8
            key = int(random.random() * (len(MiscModule.repl_dict[char]) + weight))
            if key < weight + 1:
                return MiscModule.repl_dict[char][0]  # Below weight, key equals 0 (key for first/default character)
            else:
                return MiscModule.repl_dict[char][key - weight]
        except KeyError:  # Return original char if char not found in dict
            return char

    def _return_troll(self, url):
        prefix = ''
        if 'https://' in url: prefix = 'https://'
        elif 'http://' in url: prefix = 'http://'
        return prefix + ''.join([self._select_repl(x) for x in url[len(prefix):]])

    async def troll_url(self, message):
        await self.say(message.channel, self._return_troll(message.content.split()[1]))
        await self.delete(message)

    # Used for !timedcats. May be extended for use with other commands in the future.
    # Returns a tuple (times, duration_str)
    def _parse_duration_str(self, args):
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

    async def timed_cats(self, message):
        async def inner(m):
            times, duration_str = self._parse_duration_str(m.content.split())
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
