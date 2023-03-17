'Test for db.mysql'

import unittest
import datetime

from db import MySQLDatabase, FeedContent

TESTDATA01 = FeedContent(
    content_id=None,
    feed_id=0,
    title="Test Title 1",
    url="http://example.com/test/url01",
    body="This is test contents 01",
    timestamp=datetime.datetime(2013, 01, 02, 03, 04)
)
TESTDATA02 = FeedContent(
    content_id=None,
    feed_id=0,
    title="Test Title 2",
    url="http://example.com/test/url02",
    body="This is test contents 02",
    timestamp=datetime.datetime(2013, 01, 02, 13, 14)
)
TESTDATA12 = FeedContent(
    content_id=None,
    feed_id=0,
    title="Test Title 2.1",
    url="http://example.com/test/url02",
    body="This is test contents 02.1",
    timestamp=datetime.datetime(2013, 01, 02, 14, 14)
)

class TestMySQLDatabase(unittest.TestCase):
    "test case for MySQLDatabase"
    def setUp(self):
        self.db = MySQLDatabase()
        self.db.config["database"] = "testdb"
        # self.db.create_tables()

    def tearDown(self):
        self.db.delete_all()
        # self.db.delete_tables()

    def test_append_feed_contents(self):
        self.db.append_feed_content(TESTDATA01)

    def test_append_and_get_feed_contents(self):
        feed_id = 0
        self.db.append_feed_content(TESTDATA02)
        contents = self.db.get_feed_contents(feed_id)
        urls = [x.url for x in contents]
        self.assertIn(TESTDATA02.url, urls)

        self.db.append_feed_content(TESTDATA12)
        contents = self.db.get_feed_contents(feed_id)
        self.assertIn(TESTDATA12.url, urls)
        titles = [x.title for x in contents]
        self.assertIn(TESTDATA12.title, titles)

    def test_append_feed(self):
        url = "http://example.com/"
        title = "test-title"
        self.db.append_feed(url, title)

    def test_append_and_get_feed(self):
        url = "http://example.com/test01.rss"
        title = "test-title01"
        self.db.append_feed(url, title)
        feeds = self.db.get_feeds()
        urls = [x[1] for x in feeds]
        self.assertIn(url, urls)
        titles = [x[2] for x in feeds]
        self.assertIn(title, titles)


if __name__ == '__main__':
    unittest.main()

