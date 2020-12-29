#!/usr/bin/env python3

import os
import unittest
from tmc import points

from django.test import TestCase


@points('1.4.1', '1.4.2', '1.4.3', '1.4.4', '1.4.5')
class TemplateTest(TestCase):

	def test_home(self):
		response = self.client.get('/')
		self.assertContains(response, 'Hello Template')

	def test_video(self):
		response = self.client.get('/video/')
		self.assertNotContains(response, 'Hello Template')
		self.assertContains(response, 'dQw4w9WgXcQ')
