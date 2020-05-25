Command List
============

General
^^^^^^^

!del
----
Deletes your previous message. Searches up to the previous 500 messages in the channel.

Usage
"""""
``!del``

------------------------------------------------------------------------------------------------------------------------

!google
-------
Generates a Google search link for a keyword. For lazy people like me.

Usage
"""""
* ``!google <keyword>``

------------------------------------------------------------------------------------------------------------------------

!hello
------
cakebot says hello! Use to check if cakebot is online.

Usage
"""""
* ``!hello``

------------------------------------------------------------------------------------------------------------------------

!bye
------
Turn off cakebot.

Usage
"""""
* ``!bye``

------------------------------------------------------------------------------------------------------------------------

!invite
-------
Generates a link to invite cakebot to your server

Usage
"""""
* ``!invite``

------------------------------------------------------------------------------------------------------------------------

!redirect
---------
Redirects a message to another channel.

Usage
"""""
* ``!redirect <channel mention> <message>``

Examples
""""""""
* Redirects message to #alt: ``!redirect #alt Hi guys, from the main channel!``

------------------------------------------------------------------------------------------------------------------------

!say
---------
Says a message in another channel. Requires *owner* permission.

Usage
"""""
* ``!say <channel mention> <message>``

Examples
""""""""
* Redirects message to #alt: ``!say #alt Hi guys!``

------------------------------------------------------------------------------------------------------------------------

Music
^^^^^

!musicprefix
------------

Sets the prefix for queueing music for your server's music bot.

Usage
"""""
* ``!musicprefix`` - displays the current music prefix set for the server
* ``!musicprefix <prefix>`` - sets the music prefix to <prefix>. Requires *manage_guild* or *musicprefix* permission.

The prefix can consist of multiple words.

Examples
""""""""
* Set music prefix to ``~play``: ``!musicprefix ~play``
* Set music prefix to ``! lm play``: ``!musicprefix ! lm play``

------------------------------------------------------------------------------------------------------------------------

!play
-----
Queues music using the musicprefix for the channel (check with ``!musicprefix``)

Usage
"""""
* ``!play <keyword/title/alias>``

Not case sensitive. If multiple matches are found, cakebot will display 13 possible matches and prompt the user to ``!playid``.



Variants
""""""""
* ``!play`` - Queues a song by name or alias
* ``!playid`` - Queues a song by id
* ``!playalbum`` - Queues all the songs in an album

Examples
""""""""
* Will have multiple matches: ``!play snow``
* Exact match, play song: ``!play sound of silence``
* Exact match for alias: ``!play haifuriop``

------------------------------------------------------------------------------------------------------------------------

!playalbum
----------
Queues an entire album - variant of ``!play``. The songs to be queued are displayed in the same format as !search - use !page <number> to examine.
If the songs to be queued are correct, use ``!yes`` to confirm and queue.

Usage
"""""
* ``!playalbum <name/keyword>``

Name/keyword is not case sensitive.

Examples
""""""""
* Play album named *snow halation*: ``!playalbum snow halation``

------------------------------------------------------------------------------------------------------------------------

!playid
-------
Queues a song by id - variant of ``!play``

Usage
"""""
* ``!playid <id number>``

A song's id can be found with ``!search``

Examples
""""""""
* Play song with id 316: ``!playid 316``

------------------------------------------------------------------------------------------------------------------------

!search
-------
Searches the song database for a song with a matching alias/song/artist/album name.

Usage
"""""
* ``!search <keyword>``

Displays up to 13 results at a time. Not case sensitive. If there are more than 13 results, use !page <number> to access the required page.

Examples
""""""""
* Search for songs with the kekyword snow: ``!search snow``

------------------------------------------------------------------------------------------------------------------------

!reqsong
--------
Shows links to forms for requesting songs to be added to the database.

Usage
"""""
* ``!reqsong``

------------------------------------------------------------------------------------------------------------------------

Modtools
^^^^^^^^

!logchannel
-----------
Gets or sets the channel for logging messages.

Usage
"""""
* ``!logchannel`` - displays the current channel for logging messages
* ``!logchannel set`` - sets the current channel as the logging channel. Requires *manage_guild* or *logchannel* permission.

------------------------------------------------------------------------------------------------------------------------

!purge
------
Purges a given amount of messages from the current channel. Can specify a user to purge only their messages.

Usage
"""""
* ``!purge <number>`` - purges <number> of messages in the current channel. Requires *manage_guild* permission.
* ``!purge <user mention> <number>`` - purges <number> of messages by <user mention> within the last 500 messages. Max <number> is 100. Requires *manage_guild* permission.

Examples
""""""""
* Purge last 5 messages: ``!purge 5``
* Purge Clyde's last 10 messages: ``!purge @Clyde#1234 10``

------------------------------------------------------------------------------------------------------------------------

Permissions
^^^^^^^^^^^

!permissions
------------
Gets or sets the cakebot permissions for a given user.
This does **NOT** set server permissions, but rather permissions for cakebot commands.

Permissions are required for:
* ``!musicprefix`` (set)
* ``!permissions`` (set)
* ``!logchannel`` (set)

Usage
"""""
* ``!permissions`` - displays your current cakebot permissions
* ``!permissions <user mention>`` - displays current cakebot permissions for the mentioned user
* ``permissions <user mention> <command|commands>`` - add permissionsf or the given user. Requires *manage_guild* permission.

Examples
""""""""
* Give Clyde musicprefix permissions: ``!permissions @Clyde#1234 musicprefix``
* Give Clyde musicprefix and logchannel permissions; ``!permissions @Clyde#1234 musicprefix logchannel``

------------------------------------------------------------------------------------------------------------------------

Miscellaneous
^^^^^^^^^^^^^

!timedcats
----------
Sends random cat images in timed intervals :3

Usage
"""""
* ``!timedcats <number> <interval>``

The interval can be m (minutes) or h (hours). Default number and interval is 5 m.

Examples
""""""""
* Send cat images every minute for 3 minutes: ``!timedcats 3 m``
* Send cat images every hour for 10 hours: ``!timedcats 10 h``

------------------------------------------------------------------------------------------------------------------------

!trollurl
---------
Replaces characters in a URL to make a similar looking one.

Usage
* ``!trollurl <url>``

Examples
""""""""
* Troll a Google link: ``!trollurl https://www.google.com``