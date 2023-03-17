#-*- coding: utf-8 -*-
'fetcher.py - RSS fetcher'

import feedparser
import dateutil.parser
from db import FeedContent
from datetime import datetime

def _get_attr(obj, attr, default=""):
    try:
        return obj.__getattr__(attr)
    except AttributeError:
        return default

class FeedFetcher(object):
    'Feed fetching and parsing'
    def __init__(self):
        pass

    def _fetch_and_parse(self, url):
        f = feedparser.parse(url)
        entries = []
        for e in f['entries']:
            entry = FeedContent(
                content_id=None,
                feed_id=None,
                title=_get_attr(e, "title", "(no title)"),
                url=_get_attr(e, "link"),
                body=_get_attr(e, "description"),
                timestamp=_get_attr(e, "published", None)
            )

            if entry.timestamp == None:
                entry.timestamp = _get_attr(e, "updated", None)

            if entry.timestamp == None:
                # if date is not defined, item is invalid
                continue

            # parse timestamp and convert UTC
            try:
                entry.timestamp = dateutil.parser.parse(entry.timestamp)
            except ValueError:
                entry.timestamp = datetime.now()
            if entry.timestamp.tzinfo == None:
                entry.timestamp = entry.timestamp.replace(tzinfo=dateutil.tz.tzutc())

            elif entry.timestamp.tzinfo != dateutil.tz.tzutc():
                entry.timestamp = entry.timestamp.astimezone(dateutil.tz.tzutc())

            entries.append(entry)
        return entries

    def fetch(self, url):
        'do fetch'
        entries = self._fetch_and_parse(url)
        return entries
