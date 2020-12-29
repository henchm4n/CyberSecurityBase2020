#!/usr/bin/env python3

import os
import unittest
from tmc import points
import bs4 as bs
from urllib.parse import urlsplit
from django.contrib.auth.models import User
from src.pages.models import Account
from django.test import Client

from django.test import TestCase


@points('5.1.1', '5.1.2', '5.1.3', '5.1.4', '5.1.5')
class ConfigurationTest(TestCase):

	def test_configuation(self):
		c = Client(enforce_csrf_checks=True)

		bob = User.objects.create_user(username='bob', password='squarepants')
		account = Account(user=bob, balance=100)
		account.save()

		alice = User.objects.create_user(username='alice', password='redqueen')
		account = Account(user=alice, balance=250)
		account.save()

		c.login(username='bob', password='squarepants')

		response = c.get('/transfer/', {'to': 'alice', 'amount': 10})

		bob = User.objects.get(username='bob')
		self.assertEqual(bob.account.balance, 100, "Bob's account should not change when using GET")
		bob = User.objects.get(username='alice')
		self.assertEqual(bob.account.balance, 250, "Alice's account should not change when using GET")

		response = c.post('/transfer/', {'to': 'alice', 'amount': 10})

		bob = User.objects.get(username='bob')
		self.assertEqual(bob.account.balance, 100, "Bob's account should not change when using POST without csrf token")
		bob = User.objects.get(username='alice')
		self.assertEqual(bob.account.balance, 250, "Alice's account should not change when using POST without csrf token")


		response = c.get('/')

		soup = bs.BeautifulSoup(response.content, 'html.parser')
		token = ''

		form = soup.find(id='transfer')
		self.assertEqual(form.get('method').upper().strip(), 'POST', "Transfer form method should be POST.")

		for i in form.findChildren('input'):
			if i.get('name') == 'csrfmiddlewaretoken':
				token = i.get('value')

		response = c.post('/transfer/', {'to': 'alice', 'amount': 10, 'csrfmiddlewaretoken': token})

		bob = User.objects.get(username='bob')
		self.assertEqual(bob.account.balance, 90, "Bob's account should change when using POST with csrf token")
		bob = User.objects.get(username='alice')
		self.assertEqual(bob.account.balance, 260, "Alice's account should change when using POST with csrf token")
