#!/usr/bin/python
'Test for db.mysql'

import unittest
import datetime

from db import MySQLDatabase

db = MySQLDatabase()
db.config["database"] = "testdb"
db.delete_tables()
db.create_tables()
