'Test for db.mysql'

import unittest
import datetime

from db import MySQLDatabase, FeedContent
from fetcher import FeedFetcher

class TestFetcher(unittest.TestCase):
    "test case for Fetcher"
    def setUp(self):
        self.fetcher = FeedFetcher()

    def tearDown(self):
        pass

    def test_fetch(self):
        url = "./t/testdata/test.rss"
        entries = self.fetcher.fetch(url)
        self.assertEqual(len(entries), 10)
        self.assertEqual(entries[0].url, "http://hylom.net/2012/08/08/emacs-24-on-mac-os-x/")

if __name__ == '__main__':
    unittest.main()

