#!/usr/bin/env python3

import os
import unittest
from tmc import points
from django.contrib.auth.models import User
from src.pages.models import File
import tempfile
import shutil
from io import StringIO

from django.test import TestCase, override_settings


@points('3.2.1', '3.2.2', '3.2.3', '3.2.4', '3.2.5')
class UploadTest(TestCase):

	@override_settings(MEDIA_ROOT='test/tmp')
	def test_upload(self):
		bob = User.objects.create_user(username='bob', password='squarepants')
		alice = User.objects.create_user(username='alice', password='redqueen')

		self.client.login(username='bob', password='squarepants')

		self.client.post('/add/', {'file': StringIO('Testing')})
		response = self.client.get('/download/1')
		self.assertEqual(response.content, b'Testing', "Bob can't read his own file")

		self.client.login(username='alice', password='redqueen')
		response = self.client.get('/download/1')
		self.assertNotEqual(response.content, b'Testing', "Alice should not read bob's files")

		self.client.post('/delete/', {'id': 1}, follow=True)
		self.assertEqual(File.objects.filter(owner=bob).count(), 1, "Alice should not delete bob's files")

		self.client.login(username='bob', password='squarepants')

		self.client.post('/delete/', {'id': 1}, follow=True)
		self.assertEqual(File.objects.filter(owner=bob).count(), 0)


	def tearDown(self):
		shutil.rmtree('test/tmp')
