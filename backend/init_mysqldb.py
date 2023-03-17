"Initialize MySQL Database"

from db import MySQLDatabase

d = MySQLDatabase()
d.create_tables()
