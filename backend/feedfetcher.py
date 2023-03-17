#!/usr/bin/python
"feed fetcher"

from db import MySQLDatabase
from fetcher import FeedFetcher

def main():
    db = MySQLDatabase()
    fetcher = FeedFetcher()

    feeds = db.get_feeds(offset=0, limit=10)
    read_count = 10
    while len(feeds) > 0:
        for feed in feeds:
            fid = feed[0]
            url = feed[1]
            title = feed[2]
            print "fetching #{0}: {1}".format(fid, url)
            entries = fetcher.fetch(url)
            for entry in entries:
                entry.feed_id = fid
                try:
                    print "insert {0}".format(entry.url)
                except UnicodeEncodeError:
                    print "insert {0}".format(entry.url.encode('utf-8'))
                db.append_feed_content(entry)
        feeds = db.get_feeds(offset=read_count, limit=10)
        read_count += 10

if __name__ == '__main__':
    main()
