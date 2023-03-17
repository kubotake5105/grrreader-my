'MySQL database accessor'

import sys
import mysql.connector

from base import BaseDatabase, DatabaseError, FeedContent
from config import config

class MySQLDatabase(BaseDatabase):
    "MySQL database accessor class"
    def __init__(self):
        self.config = config.get("mysql", None)
        if self.config is None:
            # no entry about MySQL connection in config.ini
            raise DatabaseError("No MySQL connection information in config file.")

    def _connect(self):
        return mysql.connector.connect(
            user = self.config["user"],
            password = self.config["password"],
            host = self.config["host"],
            port = self.config["port"],
            database = self.config["database"],
            charset = self.config["charset"]
        )

    def __enter__(self):
        self.conn = self._connect()
        self.cur = self.conn.cursor()

    def __exit__(self, type, value, tarceback):
        self.cur.close()
        self.conn.close()

    def get_feeds(self, offset=0, limit=10):
        "get RSS feeds"
        sql = """
        SELECT feed_id, url, title FROM feed_urls LIMIT %s, %s;
        """
        with self:
            self.cur.execute(sql, (offset, limit))
            result = self.cur.fetchall()
        return result

    def append_feed(self, url, default_title=""):
        "append RSS feed"
        sql = """
        SELECT * from feed_urls where url = %s;
        """
        with self:
            self.cur.execute(sql, (url,))
            if not self.cur.fetchone():
                # url is not already registers
                # insert feed
                sql = """
                INSERT INTO feed_urls
                    (url, title)
                  VALUES
                    (%s, %s);
                """
                self.cur.execute(sql, (url, default_title));

    def update_feed(self, url, default_title=""):
        "update RSS feed"
        sql = """
        UPDATE feed_urls
          SET  title = %s
          WHERE url = %s;
        """
        with self:
            self.cur.execute(sql, (default_title, url))

    def append_feed_content(self, entry):
        "append feed content"

        # check if url already exist
        with self:
            sql = """
            SELECT * from feed_contents WHERE url = %s;
            """
            params = (entry.url,)
            self.cur.execute(sql, params)
            old_val = self.cur.fetchone()
            if old_val == None:
                # url is not exist, so insert
                sql = """
                INSERT INTO feed_contents
                    (feed_id, title, url, body, timestamp)
                  VALUES
                    (%s, %s, %s, %s, %s);
                """
                params = (entry.feed_id,
                          entry.title,
                          entry.url,
                          entry.body,
                          entry.timestamp)
                self.cur.execute(sql, params)
            else:
                # url is already exist, so update
                sql = """
                UPDATE feed_contents
                  SET
                    feed_id = %s,
                    title = %s,
                    url = %s,
                    body = %s,
                    timestamp = %s
                  WHERE content_id = %s;
                """
                content_id = old_val[0]
                params = (entry.feed_id,
                          entry.title,
                          entry.url,
                          entry.body,
                          entry.timestamp,
                          content_id)
                self.cur.execute(sql, params)



    def get_feed_contents(self, feed_id, offset=0, limit=10):
        "get RSS feed's contents"
        sql = """
        SELECT * from feed_contents WHERE feed_id = %s LIMIT %s, %s;
        """
        with self:
            self.cur.execute(sql, (feed_id, offset, limit))
            results = self.cur.fetchall()
        results = [FeedContent(*x) for x in results]
        return results

    def delete_all(self):
        "delete all contents in MySQL database (for test)"
        with self:
            sql = """
            DELETE FROM feed_urls;
            """
            self.cur.execute(sql)
            sql = """
            DELETE FROM feed_contents;
            """
            self.cur.execute(sql)

    def delete_tables(self):
        "delete all tables in MySQL database (for test)"
        with self:
            sql = """
            DROP TABLE feed_urls;
            """
            self.cur.execute(sql)
            sql = """
            DROP TABLE feed_contents;
            """
            self.cur.execute(sql)
        
    def create_tables(self):
        "create tables in MySQL database"
        with self:
            sql = """
            CREATE TABLE feed_urls (
              feed_id INT PRIMARY KEY AUTO_INCREMENT,
              url     TEXT NOT NULL,
              title   TEXT
            )
            CHARACTER SET utf8;
            """
            try:
                self.cur.execute(sql)
            except mysql.connector.ProgrammingError:
                pass

            sql = """
            CREATE TABLE feed_contents (
              content_id INT PRIMARY KEY AUTO_INCREMENT,
              feed_id INT NOT NULL,
              title TEXT,
              url TEXT,
              body TEXT,
              timestamp DATETIME NOT NULL
            )
            CHARACTER SET utf8;
            """
            self.cur.execute(sql)
