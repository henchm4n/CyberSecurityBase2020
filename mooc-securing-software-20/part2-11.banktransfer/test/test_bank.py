#!/usr/bin/env python3

import os
import unittest
from unittest.mock import patch
from tmc import points

from django.test import TestCase
from src.pages.models import Account
from sqlite3 import Cursor
from django.db import connections
from django.db import connections
from django.db.backends.utils import CursorWrapper
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.conf import settings
from django.test.utils import override_settings


@points('2.5.1', '2.5.2', '2.5.3', '2.5.4', '2.5.5')
class BankTest(TestCase):

	@override_settings(DEBUG=True) # allows to see sql queries
	def test_message(self):
		ibans = ['FI5810204947291', 'FI3924290823039', 'FI4913838494922']
		balances = [125, 250, 42]
		accounts = [None] * 3


		for i, (iban, balance) in enumerate(zip(ibans, balances)):
			Account.objects.create(iban=iban, balance=balance)

		response = self.client.post('/', {'from': 'FI5810204947291', 'to': 'FI3924290823039', 'amount': 10})
		self.assertEqual(Account.objects.get(iban='FI5810204947291').balance, 115, 'Money did not move from the account during transfer')
		self.assertEqual(Account.objects.get(iban='FI3924290823039').balance, 260, 'Money did not arrive to the account during transfer')
		self.assertEqual(Account.objects.get(iban='FI4913838494922').balance, 42, 'Account should not have changed')

		response = self.client.post('/', {'from': 'FI5810204947291', 'to': 'FI3924290823039', 'amount': -10})
		self.assertEqual(Account.objects.get(iban='FI5810204947291').balance, 115, 'Negative amount transfer should not change the balance')
		self.assertEqual(Account.objects.get(iban='FI3924290823039').balance, 260, 'Negative amount transfer should not change the balance')
		self.assertEqual(Account.objects.get(iban='FI4913838494922').balance, 42, 'Negative amount transfer should not change the balance')

		response = self.client.post('/', {'from': 'FI5810204947291', 'to': 'FI3924290823039', 'amount': 1000})
		self.assertEqual(Account.objects.get(iban='FI5810204947291').balance, 115, 'Transfer larger than the balance is illegal')
		self.assertEqual(Account.objects.get(iban='FI3924290823039').balance, 260, 'Transfer larger than the balance is illegal')
		self.assertEqual(Account.objects.get(iban='FI4913838494922').balance, 42, 'Transfer larger than the balance is illegal')


		# Testing for transaction.atomic
		conn = connections['default']
		response = self.client.post('/', {'from': 'FI5810204947291', 'to': 'FI3924290823039', 'amount': 10})
		queries = [q['sql'] for q in conn.queries_log]

		# This should always succeed at this point unless the devs will change django inner logic.
		self.assertTrue(len(queries) > 0, 'Query log is empty, probably an incompatible Django version, cannot complete the test. Please inform the the course organizer.')

		self.assertTrue(queries[0].startswith('SAVEPOINT'), "First command is not wrapped in transaction.atomic, make sure that you don't have queries before the wrapper.")
		self.assertTrue(len([q for q in queries if q.startswith('SAVEPOINT')]) == 1, "Multiple transaction.atomic wrappers. You only need one.")

		ind = [i for i, q in enumerate(queries) if q.startswith('RELEASE SAVEPOINT')][0]
		self.assertTrue(len([q for q in queries[ind:] if q.startswith('INSERT') or q.startswith('UPDATE') or q.startswith('DELETE')]) == 0, "Modifications outside transaction.atomic wrapper.")
