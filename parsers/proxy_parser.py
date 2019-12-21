import requests
import random

from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool


class ProxyParser:
    def __init__(self):
        proxies = self._parse_proxies()
        self._proxies = self._check_proxies(proxies)

    def get_proxies(self):
        return self._proxies

    def get_random_proxy(self):
        if len(self._proxies) != 0:
            return random.choice(self._proxies)

    def _check_proxies(self, proxies):
        with Pool(20) as pool:
            checked_proxies = pool.map(self._check_proxy, proxies)

        active_proxies = list(filter(lambda proxy: proxy is not None, checked_proxies))

        return active_proxies

    def _check_proxy(self, proxy):
        url = 'https://ya.ru'

        try:
            requests.get(url, proxies=proxy, timeout=1)
        except requests.exceptions.RequestException:
            return None
        else:
            return proxy

    def _parse_proxies(self):
        url = 'https://free-proxy-list.net/'

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        proxy_table = soup.find('table', attrs={'id': 'proxylisttable'})
        proxy_html_list = proxy_table.find('tbody').findAll('tr')

        proxy_list = []
        for proxy in proxy_html_list:
            proxy_row = proxy.findAll('td')

            ip_address = proxy_row[0].string
            port = proxy_row[1].string
            country_code = proxy_row[2].string
            is_https = proxy_row[6].string

            if country_code == 'RU':
                if is_https == 'yes':
                    proxy_list.append({'https': 'https://{}:{}'.format(ip_address, port)})
                else:
                    proxy_list.append({'http': 'http://{}:{}'.format(ip_address, port)})

        return proxy_list
