class Song:
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
    return c.fetchmany(size=100)


def find_album(c, album):
    c.execute("SELECT * FROM songs WHERE LOWER(album) LIKE ?", ('%{}%'.format(album.lower()),))
    return c.fetchmany(size=100)


def find_song_by_id(c, song_id):
    c.execute("SELECT * FROM songs WHERE id LIKE ?", (song_id,))
    return c.fetchmany(size=1)


def search_songs(c, keyword):
    c.execute("SELECT * FROM songs "
              "WHERE LOWER(name) LIKE ? "
              "OR LOWER(album) LIKE ? "
              "OR LOWER(artist) LIKE ? "
              "OR LOWER(alias) LIKE ?", (keyword, keyword, keyword, keyword))
    return c.fetchmany(size=100)


def make_song_results(found, offset=0):
    found_size = len(found)
    if found_size == 1:
        count_str = "1 match"
    else:
        count_str = "{} matches".format(found_size)

    page_num = (offset // 13) + 1 # Integer division
    max_page_num = (found_size // 13) + 1

    results = "\nFound {} - displaying page {} of {}. Use ``!page <number>`` to access that page. Use ``!playid <id>``\n```".format(count_str, page_num, max_page_num)
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


