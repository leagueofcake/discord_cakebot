import cakebot_config
from asyncio import sleep as asyncio_sleep

from modules.ModuleInterface import ModuleInterface
from modules.helpers import is_integer
from modules.music import music_help
from modules.music.Song import Song


class MusicModule(ModuleInterface):
    def _get_music_prefix(self, server_id):
        self.c.execute("SELECT prefix FROM music_prefix WHERE server_id = ?", (server_id,))
        res = self.c.fetchone()
        if res:
            return res[0]
        return None

    def _add_music_prefix(self, server_id, new_prefix):
        self.c.execute("INSERT INTO music_prefix(server_id, prefix) VALUES (?, ?)", (server_id, new_prefix))

    def _update_music_prefix(self, server_id, new_prefix):
        self.c.execute("UPDATE music_prefix SET prefix = ? WHERE server_id = ?", (new_prefix, server_id))

    def _find_song_by_name(self, name):
        self.c.execute("SELECT * FROM songs WHERE LOWER(name) LIKE ? OR LOWER(alias) LIKE ?", (name, name))
        return self.c.fetchmany(size=100)

    async def _print_music_prefix(self, message):
        music_prefix = self._get_music_prefix(message.server.id)
        if music_prefix:
            await self.temp_message(message.channel,
                                    'Current music prefix for this server is: `{}`'.format(music_prefix))
        else:
            await self.temp_message(message.channel,
                                    'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')

    async def _set_music_prefix(self, message):
        async def inner(m):
            music_prefix = self._get_music_prefix(m.server.id)
            new_prefix = ' '.join(m.content.split()[1:])
            if music_prefix:
                self._update_music_prefix(m.server.id, new_prefix)
                await self.say(m.channel, 'Updated music prefix for this server to: `{}`'.format(new_prefix))
            else:
                self._add_music_prefix(m.server.id, new_prefix)
                await self.say(m.channel, 'Set music prefix for this server to: `{}`'.format(new_prefix))
            self.conn.commit()

        await self.auth_function(inner)(message, manage_server_auth=True, cakebot_perm='musicprefix',
                                        require_non_cakebot=True)

    def _find_album(self, album):
        self.c.execute("SELECT * FROM songs WHERE LOWER(album) LIKE ?", ('%{}%'.format(album.lower()),))
        return self.c.fetchmany(size=100)

    def _find_song_by_id(self, song_id):
        self.c.execute("SELECT * FROM songs WHERE id LIKE ?", (song_id,))
        return self.c.fetchmany(size=1)

    def _search_songs(self, keyword):
        self.c.execute("SELECT * FROM songs "
                       "WHERE LOWER(name) LIKE ? "
                       "OR LOWER(album) LIKE ? "
                       "OR LOWER(artist) LIKE ? "
                       "OR LOWER(alias) LIKE ?", (keyword, keyword, keyword, keyword))
        return self.c.fetchmany(size=100)

    def _make_song_results(self, found, offset=0):
        found_size = len(found)
        if found_size == 1:
            count_str = "1 match"
        else:
            count_str = "{} matches".format(found_size)

        page_num = (offset // 13) + 1  # Integer division
        max_page_num = (found_size // 13) + 1

        results = "\nFound {} - displaying page {} of {}. Use ``!page <number>`` to access that page. Use ``!playid <id>``\n```".format(
            count_str, page_num, max_page_num)
        results += '{:4} {:45} {:25} {:35} {:20}'.format('ID', 'Name', 'Artist', 'Album', 'Alias')  # header row

        if found:
            found = found[offset:]
            added = 0
            for res in found:
                if added == 13:
                    break
                results += '\n' + Song(*res).get_result_repr()
                added += 1
        results += '```'
        return results

    async def music_prefix(self, message):
        args = message.content.split()
        if len(args) == 1:
            await self._print_music_prefix(message)
        else:
            await self._set_music_prefix(message)

    async def _queue_songs(self, message, music_prefix, songs):
        if music_prefix:
            for song in songs:
                song = Song(*song)

                if music_prefix:
                    await self.temp_message(message.channel, '{} {}'.format(music_prefix, song.link), time=3)
                    await self.say(message.channel, '{} queued: {}'.format(message.author, song.name))
        else:
            await self.temp_message(message.channel,
                                    'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')

    async def search_and_play(self, message):
        args = message.content.split()
        command = args[0]
        prefix = self._get_music_prefix(message.server.id)
        if command == '!play' or command == '!search':
            search = '%{}%'.format(' '.join(args[1:]).lower())
            if command == '!play':
                found = self._find_song_by_name(search)
            elif command == '!search':
                found = self._search_songs(search)

            if len(found) == 1 and command == '!play':
                await self._queue_songs(message, prefix, found)
            elif len(found) > 1 or command == '!search':
                tmp = await self.say(message.channel, self._make_song_results(found))

                def check(msg):
                    splitted = msg.content.split()
                    return len(splitted) >= 2 and splitted[0] == '!page' and is_integer(splitted[1])

                msg = await self.client.wait_for_message(author=message.author, check=check,
                                                         timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                while msg is not None:
                    await self.delete(msg)
                    await self.delete(tmp)

                    page_num = msg.content.split()[1]
                    tmp = await self.say(message.channel, self._make_song_results(found, (int(page_num) - 1) * 13))
                    msg = await self.client.wait_for_message(author=message.author, check=check,
                                                             timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                await asyncio_sleep(cakebot_config.MUSIC_SEARCH_RESULT_TIME)
                await self.delete(tmp)
        else:
            found = None
            if command == '!playalbum':
                found = self._find_album(' '.join(args[1:]))
                await self.say(message.channel,
                               "Queueing the following songs. Confirm with ``!yes`` or refine your search terms.")

                def check(msg):
                    splitted = msg.content.split()
                    return msg.content == '!yes' or (
                                len(splitted) >= 2 and splitted[0] == '!page' and is_integer(splitted[1]))

                tmp = await self.say(message.channel, self._make_song_results(found))
                msg = await self.client.wait_for_message(author=message.author, check=check,
                                                         timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                while msg is not None:
                    await self.delete(msg)
                    await self.delete(tmp)

                    if msg.content == '!yes':
                        await self._queue_songs(message, prefix, found)
                        break

                    page_num = msg.content.split()[1]
                    tmp = await self.say(message.channel, self._make_song_results(found, (int(page_num) - 1) * 13))
                    msg = await self.client.wait_for_message(author=message.author, check=check,
                                                             timeout=cakebot_config.MUSIC_SEARCH_RESULT_TIME)

                await asyncio_sleep(cakebot_config.MUSIC_SEARCH_RESULT_TIME)
                await self.delete(tmp)
            elif command == '!playid':
                found = self._find_song_by_id(args[1])
                await self._queue_songs(message, prefix, found)

        if not found:
            await self.say(message.channel, "Couldn't find any matching songs!")

    async def req_song(self, message):
        await self.say(message.channel,
                       'Fill this in and PM leagueofcake: <http://goo.gl/forms/LesR4R9oXUalDRLz2>\nOr this (multiple songs): <http://puu.sh/pdITq/61897089c8.csv>')

    command_handlers = {
        '!musicprefix': music_prefix,
        '!search': search_and_play,
        '!play': search_and_play,
        '!playid': search_and_play,
        '!playalbum': search_and_play,
        '!reqsong': req_song
    }

    help_entries = music_help.help_entries
