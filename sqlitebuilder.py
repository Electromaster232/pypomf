import sqlite3
from config import Config as ConfigClass

DATABASE = ConfigClass.DATABASE


print("Building keys.db using schema.sql")
connection = sqlite3.connect("keys.db")
cur = connection.cursor()
with open('schema.sql') as fp:
    cur.executescript(fp.read())