import unittest
import requests

from parsers.yamusic_parser import YamusicParser


class YamusicParserTestCase(unittest.TestCase):
    def test_get_artist_info(self):
        yamusic_parser = YamusicParser(None, None)
        artist_info = yamusic_parser._get_artist_info(4353492)
        self.assertEqual(requests.codes.OK, artist_info.status_code)

    def test_get_artists(self):
        yamusic_parser = YamusicParser(None, None)
        artists = yamusic_parser._get_artists(None, 1)
        self.assertEqual(requests.codes.OK, artists.status_code)

    def test_parse_artists_info(self):
        yamusic_parser = YamusicParser(None, None)
        artists = [4353492, 79215]
        artists_info = yamusic_parser.parse_artists_info(artists)
        self.assertEqual(len(artists), len(artists_info))

    def test_parse_artists(self):
        yamusic_parser = YamusicParser(None, None)
        artists = yamusic_parser.parse_artists(None, 2)
        self.assertNotEqual([], artists)


if __name__ == '__main__':
    unittest.main()
