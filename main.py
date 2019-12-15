from parsers.ProxyParser import ProxyParser
from parsers.YamusicParser import YamusicParser

from pymongo import MongoClient

client = MongoClient()
database = client.yamusic_database


def save_artists():
    proxy_parser = ProxyParser()
    ya_parser = YamusicParser(None, None)
    artists = ya_parser.parse_artists(None, 101)

    artists_connection = database.artists
    artists_connection.insert(artists)


def save_artists_info():
    ya_parser = YamusicParser(None, None)

    artists = database.artists.find({}, {'_id': False, 'artist.id': True})
    artist_ids = list(map(lambda artist: artist.get('artist').get('id'), artists))

    artists_info = ya_parser.parse_artists_info(artist_ids)
    artists_info = list(filter(lambda info: info is not None, artists_info))
    artists_info_connection = database.artists_info
    artists_info_connection.insert(artists_info)


def create_graph():
    artists_info = database.artists_info.find({}, {'_id': False,
                                                   'artist.id': True,
                                                   'allSimilar': True})


if __name__ == '__main__':
    save_artists_info()
