#!/usr/bin/env python3

import unittest
from tmc import points
from tmc.utils import load

import sqlite3



module_name="src.hellodatabase"
read_database = load(module_name, "read_database")

test1_db = \
"""
CREATE TABLE Agent (id varchar(9) PRIMARY KEY,name varchar(200));
INSERT INTO Agent VALUES('Secret','Clank');
INSERT INTO Agent VALUES('Gecko','Gex');
INSERT INTO Agent VALUES('Robocod','James Pond');
INSERT INTO Agent VALUES('Fox','Sasha Nein');
INSERT INTO Agent VALUES('Riddle','Voldemort');
"""

test2_db = \
"""
CREATE TABLE Agent (id varchar(9) PRIMARY KEY, name varchar(200));
"""

test3_db = \
"""
CREATE TABLE Agent (id varchar(9) PRIMARY KEY, name varchar(200));
INSERT INTO Agent VALUES('Secret','Clank');
INSERT INTO Agent VALUES('Fox','Sasha Nein');
INSERT INTO Agent VALUES('Riddle','Voldemort');
"""


@points('2.2.1', '2.2.2', '2.2.3', '2.2.4', '2.2.5')
class DatabaseTest(unittest.TestCase):

	def test_db1(self):
		conn = sqlite3.connect(':memory:')
		conn.cursor().executescript(test1_db)
		conn.commit()
		agents = read_database(conn)
		conn.close()
		self.assertEqual(agents, [('Fox', 'Sasha Nein'), ('Gecko', 'Gex'), ('Riddle', 'Voldemort'), ('Robocod', 'James Pond'), ('Secret', 'Clank')])

	def test_db2(self):
		conn = sqlite3.connect(':memory:')
		conn.cursor().executescript(test2_db)
		conn.commit()
		agents = read_database(conn)
		conn.close()
		self.assertEqual(agents, [])

	def test_db3(self):
		conn = sqlite3.connect(':memory:')
		conn.cursor().executescript(test3_db)
		conn.commit()
		agents = read_database(conn)
		conn.close()
		self.assertEqual(agents, [('Fox', 'Sasha Nein'), ('Riddle', 'Voldemort'), ('Secret', 'Clank')])
