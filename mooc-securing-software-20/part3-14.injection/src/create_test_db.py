import sqlite3
import os

# Creates agents.sqlite
# TMC has issues with binary files, so we will go around by creating it locally from the text dump.

db = \
"""
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Users (name TEXT, password TEXT, admin BOOL);
INSERT INTO Users VALUES('admin','coffee',1);
INSERT INTO Users VALUES('bob','passwd',0);
CREATE TABLE Tasks (name TEXT, body TEXT);
INSERT INTO Tasks VALUES('bob','become admin');
INSERT INTO Tasks VALUES('admin','good to be king');
INSERT INTO Tasks VALUES('bob','profit');
COMMIT;
"""

if os.path.exists('tasks.sqlite'):
	print('tasks.sqlite already exists')
else:
	conn = sqlite3.connect('tasks.sqlite')
	conn.cursor().executescript(db)
	conn.commit()
