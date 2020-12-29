#!/usr/bin/env python3

import os
import unittest
from tmc import points
import bs4 as bs
from urllib.parse import urlsplit
from django.contrib.auth.models import User
from server.pages.models import Account

from django.test import TestCase


@points('3.5.1', '3.5.2', '3.5.3', '3.5.4', '3.5.5')
class CsrfTest(TestCase):

	def test_csrf(self):
		bob = User.objects.create_user(username='bob', password='squarepants')
		account = Account(user=bob, balance=100)
		account.save()

		alice = User.objects.create_user(username='alice', password='redqueen')
		account = Account(user=alice, balance=250)
		account.save()

		self.client.login(username='bob', password='squarepants')

		soup = bs.BeautifulSoup(open('src/csrf.html'), 'html.parser')
		imgs = soup.findAll('img')
		for img in imgs:
			url = urlsplit(img['src'])
			self.client.get(url.path + '?' + url.query, follow=True)

		bob = User.objects.get(username='bob')
		self.assertEqual(bob.account.balance, 90, "Bob's account should be 100-10=90 after csrf")
		bob = User.objects.get(username='alice')
		self.assertEqual(bob.account.balance, 260, "Alice's account should be 250+10=260 after csrf")
