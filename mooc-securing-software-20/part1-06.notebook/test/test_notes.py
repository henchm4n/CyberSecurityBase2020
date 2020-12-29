#!/usr/bin/env python3

import os
import unittest
from tmc import points
import random
import string

from django.test import TestCase

import random
import string

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


@points('1.6.1', '1.6.2', '1.6.3', '1.6.4', '1.6.5')
class NoteTest(TestCase):

	def test_adding(self):


		items = [get_random_string(10) for i in range(20)]


		for i in range(len(items)):
			response = self.client.post('/add', {'content': items[i]})
			start = max(i - 9, 0)
			for j in range(start):
				self.assertNotContains(response, items[j], msg_prefix='%d. note after %d. addition is present' % (j + 1, i + 1))

			for j in range(start, i + 1):
				self.assertContains(response, items[j], msg_prefix='%d. note after %d. addition is missing' % (j + 1, i + 1))

		response = self.client.post('/erase')
		for i in range(len(items)):
			self.assertNotContains(response, items[i], msg_prefix='%d. note after cleanup is present' % (i + 1))

		response = self.client.get('/')
		for i in range(len(items)):
			self.assertNotContains(response, items[i], msg_prefix='%d. note after cleanup and reloading is present' % (i + 1))
