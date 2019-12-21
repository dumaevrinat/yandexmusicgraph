import unittest

from parsers.proxy_parser import ProxyParser


class ProxyParserTestCase(unittest.TestCase):
    def test_initialization(self):
        proxy_parser = ProxyParser()
        self.assertNotEqual([], proxy_parser.get_proxies())

    def test_get_proxies(self):
        proxy_parser = ProxyParser()
        proxies = proxy_parser.get_proxies()
        self.assertListEqual(proxies, proxy_parser._proxies)

    def test_get_random_proxies(self):
        proxy_parser = ProxyParser()
        proxy = proxy_parser.get_random_proxy()
        self.assertIn(proxy, proxy_parser._proxies)

    def test_parse_proxies(self):
        proxy_parser = ProxyParser()
        proxies = proxy_parser._parse_proxies()
        self.assertIsInstance(proxies, list)


if __name__ == '__main__':
    unittest.main()
