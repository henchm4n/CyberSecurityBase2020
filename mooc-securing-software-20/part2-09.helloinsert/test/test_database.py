#!/usr/bin/env python3

import unittest
from tmc import points
from tmc.utils import load

import sqlite3
import os


module_name="src.hellodatabase"
read_database = load(module_name, "read_database")
add_agent = load(module_name, "add_agent")
delete_agent = load(module_name, "delete_agent")

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




@points('2.3.1', '2.3.2', '2.3.3', '2.3.4', '2.3.5')
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

	def create_test_db(self, name):
		if os.path.exists(name):
			os.remove(name)
		conn = sqlite3.connect(name)
		conn.cursor().executescript(test1_db)

	def test_add(self):
		self.create_test_db('test/tmp1.sqlite')
		conn = sqlite3.connect('test/tmp1.sqlite')
		add_agent(conn, 'Bean', 'Johnny English')
		conn.close()
		conn = sqlite3.connect('test/tmp1.sqlite')
		agents = read_database(conn)
		conn.close()
		os.remove('test/tmp1.sqlite')
		self.assertEqual(agents, [('Bean', 'Johnny English'), ('Fox', 'Sasha Nein'), ('Gecko', 'Gex'), ('Riddle', 'Voldemort'), ('Robocod', 'James Pond'), ('Secret', 'Clank')])

	def test_delete(self):
		self.create_test_db('test/tmp2.sqlite')
		conn = sqlite3.connect('test/tmp2.sqlite')
		delete_agent(conn, "Fox")
		conn.close()
		conn = sqlite3.connect('test/tmp2.sqlite')
		agents = read_database(conn)
		conn.close()
		os.remove('test/tmp2.sqlite')
		self.assertEqual(agents, [('Gecko', 'Gex'), ('Riddle', 'Voldemort'), ('Robocod', 'James Pond'), ('Secret', 'Clank')])

	def test_injection(self):
		self.create_test_db('test/tmp3.sqlite')
		conn = sqlite3.connect('test/tmp3.sqlite')
		delete_agent(conn, "Fox' OR 1=1--")
		conn.close()
		conn = sqlite3.connect('test/tmp3.sqlite')
		agents = read_database(conn)
		conn.close()
		os.remove('test/tmp3.sqlite')
		self.assertEqual(agents, [('Fox', 'Sasha Nein'), ('Gecko', 'Gex'), ('Riddle', 'Voldemort'), ('Robocod', 'James Pond'), ('Secret', 'Clank')])
