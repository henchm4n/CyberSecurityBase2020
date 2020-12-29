import sqlite3
import os

# Creates agents.sqlite
# TMC has issues with binary files, so we will go around by creating it locally from the text dump.

db = \
"""
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Agent (
    id varchar(9) PRIMARY KEY,
    name varchar(200)
);
INSERT INTO Agent VALUES('Secret','Clank');
INSERT INTO Agent VALUES('Gecko','Gex');
INSERT INTO Agent VALUES('Robocod','James Pond');
INSERT INTO Agent VALUES('Fox','Sasha Nein');
INSERT INTO Agent VALUES('Riddle','Voldemort');
COMMIT;
"""

if os.path.exists('agents.sqlite'):
	print('agents.sqlite already exists')
else:
	conn = sqlite3.connect('agents.sqlite')
	conn.cursor().executescript(db)
	conn.commit()
