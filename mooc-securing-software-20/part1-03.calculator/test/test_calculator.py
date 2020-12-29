#!/usr/bin/env python3

import os
import unittest
from tmc import points
import random

from django.test import TestCase


@points('1.3.1', '1.3.2', '1.3.3', '1.3.4', '1.3.5')
class CalculatorTest(TestCase):
	def test_add(self):
		for i in range(5):
			first = random.randrange(100, 200)
			second = random.randrange(100, 200)
			response = self.client.get('/add/', {'first': first, 'second': second})
			self.assertEqual(int(response.content.decode("utf-8")), first + second, 'Did not get expected result when adding.')

	def test_multiply(self):
		for i in range(5):
			first = random.randrange(100, 200)
			second = random.randrange(100, 200)
			response = self.client.get('/multiply/', {'first': first, 'second': second})
			self.assertEqual(int(response.content.decode("utf-8")), first * second, 'Did not get expected result when multiplying.')
