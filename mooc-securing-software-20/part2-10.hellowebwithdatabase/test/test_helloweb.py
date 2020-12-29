#!/usr/bin/env python3

import os
import unittest
import random
from tmc import points

from django.test import TestCase
from src.pages.models import Message


@points('2.4.1', '2.4.2', '2.4.3', '2.4.4', '2.4.5')
class HelloTest(TestCase):

	def test_message(self):
		messages = ['Khaaan', 'Hello there', 'Live long']
		random.shuffle(messages)

		for i, m in enumerate(messages):
			Message.objects.create(id=i, content=m)


		for i, m in enumerate(messages):
			response = self.client.get('/', {'id': i})
			self.assertEqual(response.content.decode("utf-8"), m)
