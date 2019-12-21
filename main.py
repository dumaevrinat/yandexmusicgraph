from parsers.yamusic_parser import YamusicParser

from pymongo import MongoClient

from graphviz import Graph

client = MongoClient()
database = client.yamusic_database


def save_artists():
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
    artists_info = list(database.artists_info.find({}, {'_id': False,
                                                        'artist.id': True,
                                                        'artist.name': True,
                                                        'artist.genres': True,
                                                        'allSimilar.id': True,
                                                        'likesCount': True}))

    artist_ids = set(map(lambda i: i.get('artist').get('id'), artists_info))

    dot = Graph('yamusic artists')

    for info in artists_info:
        artist_id = info.get('artist').get('id')
        artist_name = info.get('artist').get('name')
        artist_genres = info.get('artist').get('genres')
        artist_genre = artist_genres[0] if len(artist_genres) != 0 else 'default'
        likes_count = info.get('likesCount')
        similar_ids = set(map(lambda similar: similar.get('id'), info.get('allSimilar')))

        if len(similar_ids & artist_ids) > 1:
            dot.node(str(artist_id), str(artist_name), size=str(likes_count), genre=str(artist_genre))

            for similar_id in similar_ids:
                if similar_id in artist_ids:
                    dot.edge(str(artist_id), str(similar_id))

    dot.save('yamusic_artists3.gv', 'dot_output')


if __name__ == '__main__':
    create_graph()
