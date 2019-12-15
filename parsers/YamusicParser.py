import sys

import requests
import logging

from requests import HTTPError
from json import JSONDecodeError

from multiprocessing import Pool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.addHandler(handler)


class YamusicParser:
    def __init__(self, user_agents, proxy_parser):
        self._user_agents = user_agents
        self._proxy_parser = proxy_parser

    def parse_artists(self, genre_id, page_count):
        artist_info = self._get_artists(genre_id, 0).json()
        pager = artist_info.get('metatag').get('pager')
        max_page_count = pager.get('total') // pager.get('perPage')

        page_count = page_count if (page_count is not None) and (page_count <= max_page_count) else max_page_count

        artist_list = []
        for i in range(page_count):
            try:
                artist_info = self._get_artists(genre_id, i).json()
                temp_artists = artist_info.get('metatag').get('artists')

                artist_list.extend(temp_artists)
                logger.info('add {} page artist '.format(i))
            except HTTPError as e:
                logger.info('parse_artists failed with HTTPError: {}'.format(e.response))

        return artist_list

    def parse_artists_info(self, artist_id_list):
        with Pool(40) as pool:
            artists_info = list(pool.map(self._parse_artist_info, artist_id_list))

        return artists_info

    def _parse_artist_info(self, artist_id):
        try:
            return self._get_artist_info(artist_id).json()
        except HTTPError as e:
            logger.info('parse_artist_info failed with HTTPError: {}'.format(e.response))
        except JSONDecodeError as e:
            logger.info('parse_artist_info failed with JSONDecodeError: {}'.format(e.msg))
        except requests.exceptions.Timeout as e:
            logger.info('parse_artist_info failed with Timeout: {}'.format(e.response))

    def _get_artists(self, genre_id, page, use_proxy=False):
        params = {
            'id': genre_id,
            'tab': 'artists',
            'page': page,
            'sortBy': 'popular',
            'lang': 'ru'
        }

        proxies = self._proxy_parser.get_random_proxy() if use_proxy else {}

        response = requests.get('https://music.yandex.ru/handlers/metatag.jsx', params=params, proxies=proxies, timeout=5)

        if response.status_code == 200:
            return response
        else:
            raise requests.exceptions.HTTPError(response.text)

    def _get_artist_info(self, artist_id, what='info', use_proxy=False):
        params = {
            'artist': artist_id,
            'what': what,
            'lang': 'ru'
        }

        proxies = self._proxy_parser.get_random_proxy() if use_proxy else {}

        response = requests.get('https://music.yandex.ru/handlers/artist.jsx', params=params, proxies=proxies, timeout=5)

        if response.status_code == 200:
            logger.info('get {} artist info'.format(artist_id))
            return response
        else:
            logger.info('get {} artist info failed with: {}'.format(artist_id, response.text))
            raise HTTPError(response.text)
