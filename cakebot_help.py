class HelpEntry():
    def __init__(self, command, description, usage):
        self.command = command
        self.description = description
        self.usage = usage
        self.short_description = description.split('\n')[0]
    def get_entry(self):
        formatted = '\n' \
                    '**Command:** ``' + self.command + '``\n\n' \
                    '**Description**\n' + self.description + '\n\n' \
                    '**Usage**\n```' + self.usage + '```'
        return formatted

hello_desc = 'cakebot says hello!'
hello_usage = '!hello'
hello_help = HelpEntry('!hello', hello_desc, hello_usage)

timedcats_desc = 'Sends random cat images in timed intervals :3'
timedcats_usage = '!timedcats <number> <interval>\n' \
                  '<interval> - m (minute) or h (hour)\n\n' \
                  'Example: !timedcats 3 m - send random cat images each minute for 3 minutes\n' \
                  'Default is 5 m'
timedcats_help = HelpEntry('!timedcats', timedcats_desc, timedcats_usage)

find_desc = 'Searches the last 500 messages in current channel for a message containing a keyword'
find_usage = '!find <keyword> <user mention>\n' \
             '<user mention> - optional, Example:  @leagueofcake\n' \
             'Returns a message with the author of found message and timestamp.\n\n' \
             'Example: !find fruit @leagueofcake\n (user specified)' \
             'Example: !find fruit (user not specified)'
find_help = HelpEntry('!find', find_desc, find_usage)

redirect_desc = 'Redirects a message to another channel.'
redirect_usage = '!redirect <channel> <message>\n\n' \
                 '<channel> - Must be in #form Example:  #main\n\n' \
                 'Example: !redirect #alt Hi guys, from the main channel! - redirects message to #alt with message'
redirect_help = HelpEntry('!redirect', redirect_desc, redirect_usage)

play_desc = 'Queues music\n' \
            'Variants: for more info do !help <variant>\n' \
            '!play      - Queues a song by name or alias' \
            '!playid    - Queues a song by id\n' \
            '!playalbum - Queues all the songs in an album'
play_usage = '!play <keyword/title/alias>\n' \
             'Not case sensitive. If multiple matches are found, cakebot will display 15 possible matches and prompt the user to !playid <id>\n\n' \
             'Example: !play snow (will have multiple matches)\n' \
             'Example: !play sound of silence (exact match, plays song)\n' \
             'Example: !play haifuriop (exact match for alias)'
play_help = HelpEntry('!play', play_desc, play_usage)

playid_desc = 'Queues music by id\n' \
              'Variant of !play: to see other variants do !help play'
playid_usage = '!playid <id>\n' \
               '<id> - number, can be found with !search <keyword>\n\n' \
               'Example: !playid 316'
playid_help = HelpEntry('!playid', playid_desc, playid_usage)

playalbum_desc = 'Queues an entire album\n' \
                 'Variant of !play: to see other variants do !help play'
playalbum_usage = '!playalbum <name/keyword>\n' \
                  '<name> - Not case sensitive\n\n' \
                  'Example: !play snow halation'
playalbum_help = HelpEntry('!playalbum', playalbum_desc, playalbum_usage)

reqsong_desc = 'Sends link to a form for requesting songs to be added to the database.'
reqsong_usage = '!reqsong'
reqsong_help = HelpEntry('!reqsong', reqsong_desc, reqsong_usage)

search_desc = 'Searches the song database for a keyword'
search_usage = '!search <keyword>\n' \
               '<keyword> - Alias/song/artist/album name. Not case sensitive.\n\n' \
               'Example: !search snow\n' \
               'Returns up to 15 results.'
search_help = HelpEntry('!search', search_desc, search_usage)

google_desc = 'Generates a Google search link for a keyword. For lazy people like me.'
google_usage = '!google <keyword>\n'
google_help = HelpEntry('!google', google_desc, google_usage)

trollurl_desc = 'Replaces characters in a URL to make a similar looking one'
trollurl_usage = '!trollurl <url>\n'
trollurl_help = HelpEntry('!trollurl', trollurl_desc, trollurl_usage)

invite_desc = 'Generates a link to invite cakebot to your server'
invite_usage = '!invite\n'
invite_help = HelpEntry('!invite', invite_desc, invite_usage)

musicprefix_desc = 'Sets the prefix for queueing music for your server\'s music bot.'
musicprefix_usage = '!musicprefix - displays the current prefix set for the server\n' \
                    '!musicprefix <prefix>\n' \
                    'Sets the music prefix to <prefix>. Requires manage_server or musicprefix permission.\n' \
                    '<prefix> - can be multiple words.\n\n' \
                    'Example: !musicprefix ~play, !musicprefix ! lm play'
musicprefix_help = HelpEntry('!musicprefix', musicprefix_desc, musicprefix_usage)

logchannel_desc = 'Sets the channel for logging output.'
logchannel_usage = '!logchannel - displays the current channel for logging output\n' \
                   '!logchannel set - sets the current channel as the logging channel. Requires manage_server ' \
                   'or logchannel permission.'
logchannel_help = HelpEntry('!logchannel', logchannel_desc, logchannel_usage)

permissions_desc = 'Gets or sets the cakebot permissions for a given user.'
permissions_usage = 'NOTE: This does NOT set server permissions but only permissions for cakebot commands.' \
                    'Permissions are required for: !musicprefix (set), !permissions (set), !logchannel (set)' \
                    '!permissions - displays your current cakebot permissions.\n' \
                    '!permissions <user mention> - displays current cakebot permissions for the mentioned user.\n' \
                    '!permissions <user mention> <command|commands> - add permissions to the given user. Requires' \
                    'manage_server permission.' \
                    'Example: !permissions @Clyde#1234 musicprefix, !permissions @Clyde#1234 musicprefix logchannel'
permissions_help = HelpEntry('!permissions', permissions_desc, permissions_usage)

purge_desc = 'Purges a given amount of messages from the current channel.'
purge_usage = '!purge <number> - purges <number> of messages in the current channel. Requires manage_server' \
              'permission.\n' \
              '!purge <mention> <limit> - purges any messages by <mention> within the last <limit> messages. ' \
              'Requires manage_server permission\n' \
              '!cleanpurge - cleans up all purge-related messages from cakebot.' \
              'Example: !purge 5, !purge @Clyde#1234 10'
purge_help = HelpEntry('!purge', purge_desc, purge_usage)

help_desc = 'Displays this message.'
help_usage = '!help'
help_help = HelpEntry('!help', help_desc, help_usage)

help_dict = {
                'hello':     hello_help,
                'timedcats': timedcats_help,
                'find':      find_help,
                'redirect':  redirect_help,
                'play':      play_help,
                'playid':    playid_help,
                'playalbum': playalbum_help,
                'reqsong':   reqsong_help,
                'search':    search_help,
                'google':    google_help,
                'trollurl':  trollurl_help,
                'invite':    invite_help,
                'musicprefix': musicprefix_help,
                'logchannel': logchannel_help,
                'permissions': permissions_help,
                'purge': purge_help
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
