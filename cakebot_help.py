import re


class HelpEntry():
    def __init__(self, command, description, usage, category, example=None):
        self.command = command
        self.description = description
        self.usage = usage
        self.example = example
        self.category = category
        self.short_description = description.split('\n')[0]

    def get_markdown(self):
        attr = [self.description, self.usage]
        for i in range(len(attr)):
            attr[i] = re.sub(r'(!.+)(\s-\s)', r'`\1`\2', attr[i])    # Make usage command lines as code blocks
            attr[i] = re.sub(r'^(!.+)(\s-\s)?', r'`\1`\2', attr[i])  # Make usage command lines as code blocks

        marked_down = '## {}\n{}  \n\n### Usage\n{}'.format(self.command, *attr)
        if self.example:
            example = re.sub(r'(.*): (!.*)', r'\1: `\2`', self.example)  # Make example command lines as code blocks
            marked_down += '\n\n### Examples\n{}'.format(example)

        marked_down = marked_down.replace('_', '\_')     # Escape underscores
        marked_down = marked_down.replace('\n', '  \n')  # Add two spaces to end of line for Markdown line breaks
        marked_down += '  \n  \n'  # Ending newline
        return marked_down

    def get_entry(self):
        formatted = '\n' \
                    '**Command:** ``' + self.command + '``\n\n' \
                    '**Category:** ' + self.category + '\n' \
                    '**Description:** ' + self.description + '\n\n' \
                    '**Usage**\n```' + self.usage + '```\n'
        if self.example:
            formatted += '\n**Examples**\n```' + self.example + '```'

        formatted += '\nDetailed command information can be found at https://discord-cakebot.readthedocs.io/en/latest/command_list.html'
        if self.category in ['general', 'music', 'modtools', 'permissions', 'miscellaneous']:
            formatted += '#{}'.format(self.category)
        return formatted

hello_desc = 'cakebot says hello! Use to check if cakebot is online. '
hello_usage = '!hello'

timedcats_desc = 'Sends random cat images in timed intervals :3'
timedcats_usage = '!timedcats <number> <interval>\n' \
                  'The interval can be m (minutes) or h (hours).\n\n' \
                  'Default number and interval is 5 m.'
timedcats_example = 'Send cat images every minute for 3 minutes: !timedcats 3 m\n' \
                    'Send cat images every hour for 10 hours: !timedcats 10 h'

redirect_desc = 'Redirects a message to another channel.'
redirect_usage = '!redirect <channel mention> <message>'
redirect_example = 'Redirects message to #alt: !redirect #alt Hi guys, from the main channel!'

play_desc = 'Queues music using the musicprefix for the channel (check with !musicprefix)'
play_usage = '!play <keyword/title/alias>\n' \
             'Not case sensitive. If multiple matches are found, cakebot will display 13 possible matches ' \
             'and prompt the user to !playid <id>.\n\n' \
             'If there are more than 13 results, use !page <number> to access the required page.\n\n' \
             'Variants (for more info do !help <variant>)\n' \
             '!play      - Queues a song by name or alias\n' \
             '!playid    - Queues a song by id\n' \
             '!playalbum - Queues all the songs in an album'
play_example = 'Will have multiple matches: !play snow\n' \
               'Exact match, play song: !play sound of silence\n' \
               'Exact match for alias: !play haifuriop'

playid_desc = 'Queues a song by id - variant of !play'
playid_usage = '!playid <id number>\n' \
               'A song\'s id can be found with !search <keyword>'
playid_example = 'Play song with id 316: !playid 316'

playalbum_desc = 'Queues an entire album - variant of !play'
playalbum_usage = '!playalbum <name/keyword>\n' \
                  'Name/keyword is not case sensitive. The songs to be queued are displayed (similar to !search - can ' \
                  'use !page <number> to examine). \n\nIf the songs to be queued are correct, use !yes to confirm ' \
                  'and queue.'
playalbum_example = 'Play album named snow halation: !playalbum snow halation, then !yes'

reqsong_desc = 'Shows links to forms for requesting songs to be added to the database.'
reqsong_usage = '!reqsong'

search_desc = 'Searches the song database for a song with a matching alias/song/artist/album name.'
search_usage = '!search <keyword>\n\n' \
               'Displays up to 13 results at a time. Not case sensitive. If there are more than 13 results, ' \
               'use !page <number> to access the required page.'
search_example = 'Search for songs with the keyword snow: !search snow'

google_desc = 'Generates a Google search link for a keyword. For lazy people like me.'
google_usage = '!google <keyword>'

trollurl_desc = 'Replaces characters in a URL to make a similar looking one.'
trollurl_usage = '!trollurl <url>'
trollurl_example = 'Troll a Google link: !trollurl https://www.google.com'


invite_desc = 'Generates a link to invite cakebot to your server.'
invite_usage = '!invite'

musicpre_desc = 'Sets the prefix for queueing music for your server\'s music bot.'
musicpre_usage = '!musicprefix - displays the current music prefix set for the server\n' \
                 '!musicprefix <prefix> - sets the music prefix for the server to <prefix>. ' \
                 'Requires manage_server or musicprefix permission.\n\n' \
                 'The prefix can consist of multiple words.'
musicpre_example = 'Set music prefix to ~play: !musicprefix ~play\n' \
                   'Set music prefix to ! lm play: !musicprefix ! lm play'

logchannel_desc = 'Gets or sets the channel for logging messages.'
logchannel_usage = '!logchannel - displays the current channel for logging messages\n' \
                   '!logchannel set - sets the current channel as the logging channel. Requires manage_server ' \
                   'or logchannel permission.'

perms_desc = 'Gets or sets the cakebot permissions for a given user.'
perms_usage = 'NOTE: This does NOT set server permissions but only permissions for cakebot commands.\n' \
              'Permissions are required for:\n' \
              '!musicprefix (set)\n' \
              '!permissions (set)\n' \
              '!logchannel (set)\n\n' \
              '!permissions - displays your current cakebot permissions\n' \
              '!permissions <user mention> - displays current cakebot permissions for the mentioned user.\n' \
              '!permissions <user mention> <command|commands> - add permissions to the given user. Requires ' \
              'manage_server permission.'
perms_example = 'Give Clyde musicprefix permissions: !permissions @Clyde#1234 musicprefix\n' \
                'Give Clyde musicprefix and logchannel permissions: !permissions @Clyde#1234 musicprefix logchannel' \

purge_desc = 'Purges a given amount of messages from the current channel. Can purge up to 100 ' \
             'messages.'
purge_usage = '!purge <number> - purges <number> of messages in the current channel. Requires manage_server ' \
              'permission.\n' \
              '!purge <user mention> <number> - purges <number> of messages by <user mention> within the last ' \
              '500 messages. Max <number> is 100. Requires manage_server permission.'
purge_example = 'Purge last 5 messages: !purge 5\n' \
                'Purge Clyde\'s last 10 messages: !purge @Clyde#1234 10'

del_desc = 'Deletes your previous message(s). Searches up to the previous 500 messages in the ' \
           'channel. Can delete up to 100 messages.'
del_usage = '!del - delete your last message\n' \
            '!del <number> - deletes your last <number> messages'

say_desc = 'Makes cakebot talk!'
say_usage = '!say <room> <message> - makes cakebot say a message in the specified room' \

help_desc = 'Displays this message.'
help_usage = '!help'
help_help = HelpEntry('!help', help_desc, help_usage, 'general')

help_dict = {
                'hello':        HelpEntry('!hello', hello_desc, hello_usage, 'miscellaneous'),
                'timedcats':    HelpEntry('!timedcats', timedcats_desc, timedcats_usage, 'miscellaneous', timedcats_example),
                'redirect':     HelpEntry('!redirect', redirect_desc, redirect_usage, 'general', redirect_example),
                'play':         HelpEntry('!play', play_desc, play_usage, 'music', play_example),
                'playid':       HelpEntry('!playid', playid_desc, playid_usage, 'music', playid_example),
                'playalbum':    HelpEntry('!playalbum', playalbum_desc, playalbum_usage, 'music', playalbum_example),
                'reqsong':      HelpEntry('!reqsong', reqsong_desc, reqsong_usage, 'music'),
                'search':       HelpEntry('!search', search_desc, search_usage, 'general', search_example),
                'google':       HelpEntry('!google', google_desc, google_usage, 'miscellaneous'),
                'trollurl':     HelpEntry('!trollurl', trollurl_desc, trollurl_usage, 'miscellaneous'),
                'invite':       HelpEntry('!invite', invite_desc, invite_usage, 'general'),
                'musicprefix':  HelpEntry('!musicprefix', musicpre_desc, musicpre_usage, 'music', musicpre_example),
                'logchannel':   HelpEntry('!logchannel', logchannel_desc, logchannel_usage, 'modtools'),
                'permissions':  HelpEntry('!permissions', perms_desc, perms_usage, 'permissions', perms_example),
                'purge':        HelpEntry('!purge', purge_desc, purge_usage, 'modtools', purge_example),
                'del':          HelpEntry('!del', del_desc, del_usage, 'general'),
                'say':          HelpEntry('!say', say_desc, say_usage, 'miscellaneous')
            }


# Interface functions
def get_entry(name):
    return help_dict[name].get_entry()


def generate_summary():
    sorted_keys = sorted(help_dict)
    head = '\nCommand summary. For more information do ``!help <command>`` e.g. ``!help timedcats``\n'
    summary = head
    summary += '```'
    for command in sorted_keys:
        summary += help_dict[command].command.ljust(14, ' ')
        summary += help_dict[command].short_description + '\n'
    summary += '```'

    summary += '\nFull command list can be found at https://discord-cakebot.readthedocs.io/en/latest/command_list.html'
    return summary
