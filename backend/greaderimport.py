#!/usr/bin/python
# -*- coding: utf-8 -*-
"feed fetcher"

from db import MySQLDatabase
import xml.parsers.expat
import sys

mysql_db = MySQLDatabase()

def StartElementHandler(name, attr):
    if name == "outline":
        url = attr["xmlUrl"]
        title = attr["title"]
        print u"add feed: {0} as {1}".format(url, title)
        mysql_db.append_feed(url, title)
        #mysql_db.update_feed(url, title)

def main():
    parser = xml.parsers.expat.ParserCreate('utf-8')
    parser.StartElementHandler = StartElementHandler
    parser.ParseFile(sys.stdin)

if __name__ == '__main__':
    main()
