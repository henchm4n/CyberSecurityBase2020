#!/usr/bin/env python3

import unittest
from tmc import points
from tmc.utils import load

import sqlite3
import random
import string



module_name="src.injection"
query = load(module_name, "query")


@points('3.1.1', '3.1.2', '3.1.3', '3.1.4', '3.1.5')
class InjectionTest(unittest.TestCase):

	def test_injection(self):
		conn = sqlite3.connect(':memory:')
		cursor = conn.cursor()
		passwd = ''.join(random.choice(string.ascii_lowercase) for i in range(8))

		cursor.execute("CREATE TABLE Users (name TEXT, password TEXT, admin BOOL)")
		cursor.execute("INSERT INTO Users VALUES('admin',?,1)", [passwd])
		cursor.execute("INSERT INTO Users VALUES('bob','passwd',0)")
		cursor.execute("CREATE TABLE Tasks (name TEXT, body TEXT)")
		cursor.execute("INSERT INTO Tasks VALUES('bob','become admin')")
		cursor.execute("INSERT INTO Tasks VALUES('admin','good to be king')")
		cursor.execute("INSERT INTO Tasks VALUES('bob','profit')")
		conn.commit()

		response = [x[0] for x in cursor.execute("SELECT body FROM Tasks WHERE name='%s' and body LIKE '%%%s%%'" % ('bob', query())).fetchall()]

		self.assertEqual(response, [passwd])
