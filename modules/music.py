from .helpers import temp_message


class Song():
    def __init__(self, song_id, name, artist, album, link, alias):
        self.song_id = song_id
        self.name = name
        self.artist = artist
        self.album = album
        self.link = link
        self.alias = alias

    def get_result_repr(self):
        args = [self.song_id, self.name, self.artist, self.album, self.alias]
        args = [str(arg) for arg in args]
        return "{:4} {:45.45} {:25.25} {:35.35} {:20.20}".format(*args)


def get_music_prefix(c, server_id):
    c.execute("SELECT prefix FROM music_prefix WHERE server_id = ?", (server_id, ))
    res = c.fetchone()
    if res:
        return res[0]
    return None


def add_music_prefix(c, server_id, new_prefix):
    c.execute("INSERT INTO music_prefix(server_id, prefix) VALUES (?, ?)", (server_id, new_prefix))


def update_music_prefix(c, server_id, new_prefix):
    c.execute("UPDATE music_prefix SET prefix = ? WHERE server_id = ?", (new_prefix, server_id))


def find_song_by_name(c, name):
    c.execute("SELECT * FROM songs WHERE LOWER(name) LIKE ? OR LOWER(alias) LIKE ?", (name, name))
    return c.fetchmany(size=13)


def find_album(c, album):
    c.execute("SELECT * FROM songs WHERE LOWER(album) LIKE ?", ('%{}%'.format(album.lower()),))
    return c.fetchmany(size=13)


def find_song_by_id(c, song_id):
    c.execute("SELECT * FROM songs WHERE id LIKE ?", (song_id,))
    return c.fetchmany(size=1)


def search_songs(c, keyword):
    c.execute("SELECT * FROM songs "
              "WHERE LOWER(name) LIKE ? "
              "OR LOWER(album) LIKE ? "
              "OR LOWER(artist) LIKE ? "
              "OR LOWER(alias) LIKE ?", (keyword, keyword, keyword, keyword))
    return c.fetchmany(size=13)


def make_song_results(found):
    if len(found) == 1:
        count_str = "1 match"
    else:
        count_str = "{} matches".format(len(found))

    results = "\nFound {}: (limited to 13). Use ``!playid <id>``\n```".format(count_str)
    results += '{:4} {:45} {:25} {:35} {:20}'.format('ID', 'Name', 'Artist', 'Album', 'Alias')  # header row

    if found:
        for res in found:
            results += '\n' + Song(*res).get_result_repr()
    results += '```'
    return results


async def queue_songs(client, message, music_prefix, songs):
    if music_prefix:
        for song in songs:
            song = Song(*song)

            if music_prefix:
                await temp_message(client, message.channel, '{} {}'.format(music_prefix, song.link), time=3)
                await client.send_message(message.channel, '{} queued: {}'.format(message.author, song.name))
    else:
        await temp_message(client, message.channel,
                           'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')
