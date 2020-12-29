#!/usr/bin/env python3

import os
import unittest
import uuid
import random
from tmc import points
from tmc.utils import load

from django.test import LiveServerTestCase

from django.contrib.auth import get_user_model


module_name="src.hackpassword"
test_password = load(module_name, "test_password")


@points('4.1.1', '4.1.2', '4.1.3', '4.1.4', '4.1.5')
class HackTest(LiveServerTestCase):

	def setUp(self):
		self.candidates = [str(uuid.uuid1())[:16] for i in range(20)]
		self.passwd = self.candidates[random.randrange(5, 15)]
		User = get_user_model()
		User.objects.create_superuser('admin', 'admin@admin.gov', self.passwd)


	def test_hack(self):
		self.assertEqual(test_password(self.live_server_url, self.candidates), self.passwd)
