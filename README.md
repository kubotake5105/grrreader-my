Grrreader - test2
=========

Grrreader - Gxxgle-Reader-inspired Rss READER
(a.k.a. Gxxgle Reader Clone)


What is "grrreader"?
-------------------

Grrreader is Web-based RSS reader application. Grrreader has
Gxxgle-Reader-like AJAX based UI, independent RSS feed fetcher,
and minimal feature to check RSSs are implemented.

Grrreader uses Python to fetch RSS feed, and Node.js to build HTTP Server
and Web UI.


Requires
--------
 * Python 2.7.x
 * Node.js 0.10.x
 * Some python modules: "feedparser", "dateutil.parser", "mysql.connector"
 * Some node.js modules: defined in client/package.json and "forever"
 * MySQL


How to install
--------------

1. install Python (>2.7.x), Node.js (>0.10.x), MySQL
2. create MySQL database and user, tables for use
3. run `npm install` in client directory
4. copy client/config.json.sample to client/config.json
5. edit client/config.json
6. copy backend/config.ini.sample to backend/config.ini
7. edit backend/config.ini
8. fix 'DEST' line to install directory for client in install.sh
9. execute backend/feedfetcher.py to initial feed fetching
10. add backend/feedfetcher.py to crontab
11. start rrreader service like: `# service grreader start`

Create Tables
---------------
To create Tables, do below commands.

    $ cd backend
    $ python
    Python 2.7.2 (default, Oct 11 2012, 20:14:37) 
    [GCC 4.2.1 Compatible Apple Clang 4.0 (tags/Apple/clang-418.0.60)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import db
    >>> db.MySQLDatabase().create_tables()
    >>> ^D
    $


Import Google Reader's registered feeds
---------------------------------------
    $ cd backend
    $ python greaderimport.py < ../subscriptions.xml  


Sample crontab
--------------
    # MM HH DD MM WE CMD
    */30   *  *  *  *  cd /usr/local/share/grrreadder/backend; /usr/bin/python feedfetcher.py > /dev/null


