# discord_cakebot
General-purpose bot for discord.

## Command List
## !del  
Deletes your previous message. Searches up to the previous 500 messages in the channel.    
  
### Usage  
`!del`  
  
## !find  
Searches the last 500 messages in current channel for a message containing a keyword.    
  
### Usage  
`!find <keyword>` - find a message with the specified keyword  
`!find <keyword> <user mention>` - find a message with specified keyword by specified user  
Returns a message with the author of the most rececnt matching message and its timestamp if found.  
  
### Examples  
User specified: `!find cake @leagueofcake#1234`  
User not specified: `!find cake`  
  
## !google  
Generates a Google search link for a keyword. For lazy people like me.    
  
### Usage  
`!google <keyword>`  
  
## !hello  
cakebot says hello! Use to check if cakebot is online.     
  
### Usage  
`!hello`  
  
## !invite  
Generates a link to invite cakebot to your server.    
  
### Usage  
`!invite`  
  
## !logchannel  
Gets or sets the channel for logging messages.    
  
### Usage  
`!logchannel` - displays the current channel for logging messages  
`!logchannel set` - sets the current channel as the logging channel. Requires manage\_server or logchannel permission.  
  
## !musicprefix  
Sets the prefix for queueing music for your server's music bot.    
  
### Usage  
`!musicprefix` - displays the current music prefix set for the server  
`!musicprefix <prefix>` - sets the music prefix for the server to <prefix>. Requires manage\_server or musicprefix permission.  
  
The prefix can consist of multiple words.  
  
### Examples  
Set music prefix to ~play: `!musicprefix ~play`  
Set music prefix to ! lm play: `!musicprefix ! lm play`  
  
## !permissions  
Gets or sets the cakebot permissions for a given user.    
  
### Usage  
NOTE: This does NOT set server permissions but only permissions for cakebot commands.  
Permissions are required for:  
!musicprefix (set)  
!permissions (set)  
!logchannel (set)  
  
`!permissions` - displays your current cakebot permissions  
`!permissions <user mention>` - displays current cakebot permissions for the mentioned user.  
`!permissions <user mention> <command|commands>` - add permissions to the given user. Requires manage\_server permission.  
  
### Examples  
Give Clyde musicprefix permissions: `!permissions @Clyde#1234 musicprefix`  
Give Clyde musicprefix and logchannel permissions: `!permissions @Clyde#1234 musicprefix logchannel`  
  
## !play  
Queues music using the musicprefix for the channel (check with !musicprefix)    
  
### Usage  
`!play <keyword/title/alias>`  
Not case sensitive. If multiple matches are found, cakebot will display 13 possible matches and prompt the user to !playid <id>  
  
Variants (for more info do !help <variant>)  
`!play     ` - Queues a song by name or alias  
`!playid   ` - Queues a song by id  
`!playalbum` - Queues all the songs in an album  
  
### Examples  
Will have multiple matches: `!play snow`  
Exact match, play song: `!play sound of silence`  
Exact match for alias: `!play haifuriop`  
  
## !playalbum  
Queues an entire album - variant of !play    
  
### Usage  
`!playalbum <name/keyword>`  
Name/keyword is not case sensitive.  
  
### Examples  
Play album named snow halation: `!play snow halation`  
  
## !playid  
Queues a song by id - variant of !play    
  
### Usage  
`!playid <id number>`  
A song's id can be found with !search <keyword>  
  
### Examples  
Play song with id 316: `!playid 316`  
  
## !purge  
Purges a given amount of messages from the current channel.    
  
### Usage  
`!purge <number>` - purges <number> of messages in the current channel. Requires manage\_server permission.  
`!purge <user mention> <number>` - purges <number> of messages by <user mention> within the last 500 messages. Requires manage\_server permission.  
  
### Examples  
Purge last 5 messages: `!purge 5`  
Purge Clyde's last 10 messages: `!purge @Clyde#1234 10`  
  
## !redirect  
Redirects a message to another channel.    
  
### Usage  
`!redirect <channel mention> <message>`  
  
### Examples  
Redirects message to #alt: `!redirect #alt Hi guys, from the main channel!`  
  
## !reqsong  
Shows links to forms for requesting songs to be added to the database.    
  
### Usage  
`!reqsong`  
  
## !search  
Searches the song database for a song with a matching alias/song/artist/album name.    
  
### Usage  
`!search <keyword>`  
  
Returns up to 13 results. Not case sensitive.  
  
### Examples  
Search for songs with the keyword snow: `!search snow`  
  
## !timedcats  
Sends random cat images in timed intervals :3    
  
### Usage  
`!timedcats <number> <interval>`  
The interval can be m (minutes) or h (hours).  
  
Default number and interval is 5 m.  
  
### Examples  
Send cat images every minute for 3 minutes: `!timedcats 3 m`  
Send cat images every hour for 10 hours: `!timedcats 10 h`  
  
## !trollurl  
Replaces characters in a URL to make a similar looking one.    
  
### Usage  
`!trollurl <url>`  
  
