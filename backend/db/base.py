'Database base class'

class BaseDatabase(object):
    pass


class FeedContent(object):
    def __init__(self, content_id, feed_id, title, url, body, timestamp):
        self.content_id = content_id
        self.feed_id = feed_id
        self.title = title
        self.url = url
        self.body = body
        self.timestamp = timestamp


class FeedContentError(Exception):
    "Error class for feed content"
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class DatabaseError(Exception):
    "Error class for database"
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


