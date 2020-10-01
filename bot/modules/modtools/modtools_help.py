from bot.modules.HelpEntry import HelpEntry

_logchannel_desc = 'Gets or sets the channel for logging messages.'
_logchannel_usage = '!logchannel - displays the current channel for logging messages\n' \
                   '!logchannel set - sets the current channel as the logging channel. Requires manage_guild ' \
                   'or logchannel permission.'


_purge_desc = 'Purges a given amount of messages from the current channel. Can purge up to 100 ' \
             'messages.'
_purge_usage = '!purge <number> - purges <number> of messages in the current channel. Requires manage_guild ' \
              'permission.\n' \
              '!purge <user mention> <number> - purges <number> of messages by <user mention> within the last ' \
              '500 messages. Max <number> is 100. Requires manage_guild permission.'
_purge_example = 'Purge last 5 messages: !purge 5\n' \
                'Purge Clyde\'s last 10 messages: !purge @Clyde#1234 10'

_del_desc = 'Deletes your previous message(s). Searches up to the previous 500 messages in the ' \
           'channel. Can delete up to 100 messages.'
_del_usage = '!del - delete your last message\n' \
            '!del <number> - deletes your last <number> messages'

help_entries = {
    'logchannel':   HelpEntry('!logchannel', _logchannel_desc, _logchannel_usage, 'modtools'),
    'purge':        HelpEntry('!purge', _purge_desc, _purge_usage, 'modtools', _purge_example),
    'del':          HelpEntry('!del', _del_desc, _del_usage, 'general'),
}

