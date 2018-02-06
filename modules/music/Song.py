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

