class HelpEntry():
    def __init__(self, command, description, usage, category, example=None):
        self.command = command
        self.description = description
        self.usage = usage
        self.example = example
        self.category = category
        self.short_description = description.split('\n')[0]
    def get_entry(self):
        formatted = '\n' \
                    '**Command:** ``' + self.command + '``\n\n' \
                    '**Category:** ' + self.category + '\n' \
                    '**Description:** ' + self.description + '\n\n' \
                    '**Usage**\n```' + self.usage + '```\n\n'
        if self.example:
            formatted += '**Examples**\n```' + self.example + '```'
        return formatted

hello_desc = 'cakebot says hello!'
hello_usage = '!hello'

timedcats_desc = 'Sends random cat images in timed intervals :3'
timedcats_usage = '!timedcats <number> <interval>\n' \
                  '<interval> - m (minute) or h (hour)\n\n' \
                  'Default interval is 5 m.'
timedcats_example = 'Send cat images for 3 minutes: !timedcats 3 m' \

find_desc = 'Searches the last 500 messages in current channel for a message containing a keyword.'
find_usage = '!find <keyword> <user mention>\n' \
             'NOTE: <user mention> is optional, Example:  @leagueofcake\n' \
             'Returns a message with the author of found message and timestamp.\n\n'
find_example = 'User specified: !find fruit @leagueofcake#1234\n' \
               'User not specified: Example: !find fruit'

redirect_desc = 'Redirects a message to another channel.'
redirect_usage = '!redirect <channel> <message>\n\n' \
                    '<channel> - Must be in channel mention \n\n'
redirect_example = 'Redirects message to #alt with message: !redirect #alt Hi guys, from the main channel!'

play_desc = 'Queues music using the musicprefix for the channel (check with !musicprefix)'
play_usage = '!play <keyword/title/alias>\n' \
             'Not case sensitive. If multiple matches are found, cakebot will display 15 possible matches ' \
             'and prompt the user to !playid <id>\n\n' \
             'Variants (for more info do !help <variant>)\n' \
             '!play      - Queues a song by name or alias\n' \
             '!playid    - Queues a song by id\n' \
             '!playalbum - Queues all the songs in an album'
play_example = 'Will have multiple matches: !play snow\n' \
               'Exact match, play song: !play sound of silence\n' \
               'Exact match for alias: !play haifuriop'

playid_desc = 'Queues music by id - variant of !play'
playid_usage = '!playid <id>\n' \
               '<id> - number, can be found with !search <keyword>\n\n'
playid_example = 'Play song with id 316: !playid 316'

playalbum_desc = 'Queues an entire album - variant of !play'
playalbum_usage = '!playalbum <name/keyword>\n' \
                  '<name> - Not case sensitive\n\n'
playalbum_example = 'Play album named snow halation: !play snow halation'

reqsong_desc = 'Shows links to forms for requesting songs to be added to the database.'
reqsong_usage = '!reqsong'

search_desc = 'Searches the song database for a keyword'
search_usage = '!search <keyword>\n' \
               '<keyword> - Alias/song/artist/album name. Not case sensitive.\n\n' \
               'Returns up to 15 results.'
search_example = 'Search for songs with the keyword snow: !search snow'

google_desc = 'Generates a Google search link for a keyword. For lazy people like me.'
google_usage = '!google <keyword>'

trollurl_desc = 'Replaces characters in a URL to make a similar looking one'
trollurl_usage = '!trollurl <url>'


invite_desc = 'Generates a link to invite cakebot to your server'
invite_usage = '!invite'

musicpre_desc = 'Sets the prefix for queueing music for your server\'s music bot.'
musicpre_usage = '!musicprefix - displays the current prefix set for the server\n' \
                 '!musicprefix <prefix> - ' \
                 'Sets the music prefix to <prefix>. Requires manage_server or musicprefix permission.\n' \
                 'NOTE: <prefix> - can be multiple words.\n\n'
musicpre_example = 'Set music prefix to ~play: !musicprefix ~play\n' \
                   'Set music prefix to ! lm play: !musicprefix ! lm play'

logchannel_desc = 'Sets the channel for logging output.'
logchannel_usage = '!logchannel - displays the current channel for logging output\n' \
                   '!logchannel set - sets the current channel as the logging channel. Requires manage_server ' \
                   'or logchannel permission.'

perms_desc = 'Gets or sets the cakebot permissions for a given user.'
perms_usage = 'NOTE: This does NOT set server permissions but only permissions for cakebot commands.\n' \
              'Permissions are required for:\n' \
              '!musicprefix (set)\n' \
              '!permissions (set)\n' \
              '!logchannel (set)\n\n' \
              '!permissions - displays your current cakebot permissions.\n' \
              '!permissions <user mention> - displays current cakebot permissions for the mentioned user.\n' \
              '!permissions <user mention> <command|commands> - add permissions to the given user. Requires ' \
              'manage_server permission.'
perms_example = 'Give Clyde musicprefix permissions: !permissions @Clyde#1234 musicprefix\n' \
                'Give Clyde musicprefix and logchannel permissions: !permissions @Clyde#1234 musicprefix logchannel' \

purge_desc = 'Purges a given amount of messages from the current channel.'
purge_usage = '!purge <number> - purges <number> of messages in the current channel. Requires manage_server' \
              'permission.\n' \
              '!purge <mention> <number> - purges <number> of messages by <mention> within the last 500 messages. ' \
              'Requires manage_server permission\n' \
              '!cleanpurge - cleans up all purge-related messages from cakebot.'
purge_example = 'Purge last 5 messages: !purge 5\n' \
                'Purge Clyde\'s last 10 messages: !purge @Clyde#1234 10'

del_desc = 'Deletes your previous message. Searches up to the previous 500 messages in the channel.'
del_usage = '!del - Deletes your previous message.\n' \

help_desc = 'Displays this message.'
help_usage = '!help'
help_help = HelpEntry('!help', help_desc, help_usage, 'general')

help_dict = {
                'hello':        HelpEntry('!hello', hello_desc, hello_usage, 'misc'),
                'timedcats':    HelpEntry('!timedcats', timedcats_desc, timedcats_usage, 'misc', timedcats_example),
                'find':         HelpEntry('!find', find_desc, find_usage, 'general', find_example),
                'redirect':     HelpEntry('!redirect', redirect_desc, redirect_usage, 'general', redirect_example),
                'play':         HelpEntry('!play', play_desc, play_usage, 'music', play_example),
                'playid':       HelpEntry('!playid', playid_desc, playid_usage, 'music', playid_example),
                'playalbum':    HelpEntry('!playalbum', playalbum_desc, playalbum_usage, 'music', playalbum_example),
                'reqsong':      HelpEntry('!reqsong', reqsong_desc, reqsong_usage, 'music'),
                'search':       HelpEntry('!search', search_desc, search_usage, 'general', search_example),
                'google':       HelpEntry('!google', google_desc, google_usage, 'misc'),
                'trollurl':     HelpEntry('!trollurl', trollurl_desc, trollurl_usage, 'misc'),
                'invite':       HelpEntry('!invite', invite_desc, invite_usage, 'general'),
                'musicprefix':  HelpEntry('!musicprefix', musicpre_desc, musicpre_usage, 'music', musicpre_example),
                'logchannel':   HelpEntry('!logchannel', logchannel_desc, logchannel_usage, 'modtools'),
                'permissions':  HelpEntry('!permissions', perms_desc, perms_usage, 'modtools', perms_example),
                'purge':        HelpEntry('!purge', purge_desc, purge_usage, 'modtools', purge_example),
                'del':          HelpEntry('!del', del_desc, del_usage, 'general')
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
    return summary
