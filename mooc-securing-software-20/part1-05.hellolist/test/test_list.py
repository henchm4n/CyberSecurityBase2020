#!/usr/bin/env python3

import os
import unittest
from tmc import points

from django.test import TestCase


@points('1.5.1', '1.5.2', '1.5.3', '1.5.4', '1.5.5')
class TemplateTest(TestCase):

	def test_adding(self):

		items = ["Abracadabra", "Alakazam", "Bibbidi-Bobbidi-Boo", "By the Power of Grayskull, I HAVE THE POWER", "Open sesame", "Shazam", "Expecto Patronum"]

		response = self.client.get('/')

		for i in range(len(items)):
			self.assertNotContains(response, items[i])

		for i in range(len(items)):
			response = self.client.post('/', {'content': items[i]})
			for j in range(i + 1):
				self.assertContains(response, items[j])
			for j in range(i + 1, len(items)):
				self.assertNotContains(response, items[j])
