import random

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


def select_repl(char):
    try:
        weight = 8
        key = int(random.random() * (len(repl_dict[char]) + weight))
        if key < weight + 1:
            return repl_dict[char][0]  # Below weight, key equals 0 (key for first/default character)
        else:
            return repl_dict[char][key - weight]
    except KeyError:  # Return original char if char not found in dict
        return char


def return_troll(url):
    prefix = ''
    if 'https://' in url: prefix = 'https://'
    elif 'http://' in url: prefix = 'http://'
    return prefix + ''.join([select_repl(x) for x in url[len(prefix):]])