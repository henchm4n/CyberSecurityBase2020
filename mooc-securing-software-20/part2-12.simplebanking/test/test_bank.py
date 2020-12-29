#!/usr/bin/env python3

import unittest
from tmc import points
from django.contrib.auth.models import User
from src.pages.models import Account
import bs4 as bs
import uuid


from django.test import TestCase



@points('2.6.1', '2.6.2', '2.6.3', '2.6.4', '2.6.5')
class BankTest(TestCase):

	def get_accounts(self, response):
		soup = bs.BeautifulSoup(response.content, 'html.parser')
		accounts = []
		for i in soup.ul.findChildren('li'):
			accounts.append(i.get_text().strip())
		return accounts

	def test_bank(self):
		bob = User.objects.create_user(username='bob', password='squarepants')
		alice = User.objects.create_user(username='alice', password='redqueen')

		self.client.login(username='bob', password='squarepants')
		iban1 = str(uuid.uuid4())
		iban2 = str(uuid.uuid4())
		iban3 = str(uuid.uuid4())
		response = self.client.post('/add/', {'iban': iban1}, follow=True)
		response = self.client.post('/add/', {'iban': iban2}, follow=True)
		response = self.client.post('/add/', {'iban': iban3}, follow=True)

		self.assertCountEqual(self.get_accounts(response), [iban1, iban2, iban3])

		self.client.login(username='alice', password='redqueen')
		iban1 = str(uuid.uuid4())
		iban2 = str(uuid.uuid4())
		response = self.client.post('/add/', {'iban': iban1}, follow=True)
		response = self.client.post('/add/', {'iban': iban2}, follow=True)

		self.assertCountEqual(self.get_accounts(response), [iban1, iban2])
