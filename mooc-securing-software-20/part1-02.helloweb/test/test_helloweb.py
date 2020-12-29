#!/usr/bin/env python3

import os
import unittest
from tmc import points

from django.test import TestCase


@points('1.2.1', '1.2.2', '1.2.3', '1.2.4', '1.2.5')
class HelloTest(TestCase):

	def test_home(self):
		response = self.client.get('/')
		self.assertEqual(response.content.decode("utf-8"), 'Hello Web!', 'The greeting message is incorrect')
