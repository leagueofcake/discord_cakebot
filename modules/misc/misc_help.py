from modules.HelpEntry import HelpEntry

_timedcats_desc = 'Sends random cat images in timed intervals :3'
_timedcats_usage = '!timedcats <number> <interval>\n' \
                  'The interval can be m (minutes) or h (hours).\n\n' \
                  'Default number and interval is 5 m.'
_timedcats_example = 'Send cat images every minute for 3 minutes: !timedcats 3 m\n' \
                    'Send cat images every hour for 10 hours: !timedcats 10 h'

_trollurl_desc = 'Replaces characters in a URL to make a similar looking one.'
_trollurl_usage = '!trollurl <url>'
_trollurl_example = 'Troll a Google link: !trollurl https://www.google.com'

_invite_desc = 'Generates a link to invite cakebot to your server.'
_invite_usage = '!invite'

_google_desc = 'Generates a Google search link for a keyword. For lazy people like me.'
_google_usage = '!google <keyword>'

help_entries = {
    'timedcats':    HelpEntry('!timedcats', _timedcats_desc, _timedcats_usage, 'miscellaneous', _timedcats_example),
    'trollurl':     HelpEntry('!trollurl', _trollurl_desc, _trollurl_usage, 'miscellaneous'),
    'invite':       HelpEntry('!invite', _invite_desc, _invite_usage, 'general'),
    'google':       HelpEntry('!google', _google_desc, _google_usage, 'miscellaneous'),
}
