from modules.HelpEntry import HelpEntry

_play_desc = 'Queues music using the musicprefix for the channel (check with !musicprefix)'
_play_usage = '!play <keyword/title/alias>\n' \
             'Not case sensitive. If multiple matches are found, cakebot will display 13 possible matches ' \
             'and prompt the user to !playid <id>.\n\n' \
             'If there are more than 13 results, use !page <number> to access the required page.\n\n' \
             'Variants (for more info do !help <variant>)\n' \
             '!play      - Queues a song by name or alias\n' \
             '!playid    - Queues a song by id\n' \
             '!playalbum - Queues all the songs in an album'
_play_example = 'Will have multiple matches: !play snow\n' \
               'Exact match, play song: !play sound of silence\n' \
               'Exact match for alias: !play haifuriop'

_playid_desc = 'Queues a song by id - variant of !play'
_playid_usage = '!playid <id number>\n' \
               'A song\'s id can be found with !search <keyword>'
_playid_example = 'Play song with id 316: !playid 316'

_playalbum_desc = 'Queues an entire album - variant of !play'
_playalbum_usage = '!playalbum <name/keyword>\n' \
                  'Name/keyword is not case sensitive. The songs to be queued are displayed (similar to !search - can ' \
                  'use !page <number> to examine). \n\nIf the songs to be queued are correct, use !yes to confirm ' \
                  'and queue.'
_playalbum_example = 'Play album named snow halation: !playalbum snow halation, then !yes'

_reqsong_desc = 'Shows links to forms for requesting songs to be added to the database.'
_reqsong_usage = '!reqsong'

_search_desc = 'Searches the song database for a song with a matching alias/song/artist/album name.'
_search_usage = '!search <keyword>\n\n' \
               'Displays up to 13 results at a time. Not case sensitive. If there are more than 13 results, ' \
               'use !page <number> to access the required page.'
_search_example = 'Search for songs with the keyword snow: !search snow'

_musicpre_desc = 'Sets the prefix for queueing music for your server\'s music bot.'
_musicpre_usage = '!musicprefix - displays the current music prefix set for the server\n' \
                 '!musicprefix <prefix> - sets the music prefix for the server to <prefix>. ' \
                 'Requires manage_guild or musicprefix permission.\n\n' \
                 'The prefix can consist of multiple words.'
_musicpre_example = 'Set music prefix to ~play: !musicprefix ~play\n' \
                   'Set music prefix to ! lm play: !musicprefix ! lm play'

help_entries = {
    'musicprefix':  HelpEntry('!musicprefix', _musicpre_desc, _musicpre_usage, 'music', _musicpre_example),
    'search':       HelpEntry('!search', _search_desc, _search_usage, 'general', _search_example),
    'play':         HelpEntry('!play', _play_desc, _play_usage, 'music', _play_example),
    'playid':       HelpEntry('!playid', _playid_desc, _playid_usage, 'music', _playid_example),
    'playalbum':    HelpEntry('!playalbum', _playalbum_desc, _playalbum_usage, 'music', _playalbum_example),
    'reqsong':      HelpEntry('!reqsong', _reqsong_desc, _reqsong_usage, 'music'),
}
