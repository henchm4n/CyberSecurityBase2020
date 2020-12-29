#!/usr/bin/env python3

import unittest
from tmc import points
from tmc.utils import load, get_out

import io
import sys
import uuid



module_name="src.list_vulnerabilities"
get_vulnerabilities = load(module_name, "get_vulnerabilities")


@points('3.4.1', '3.4.2', '3.4.3', '3.4.4', '3.4.5')
class SafetyScanner(unittest.TestCase):

	def test_simple(self):
		db = open('test/snippet.json')
		result = get_vulnerabilities('acqusition', db)
		db.close()
		self.assertEqual(result, [('pyup.io-34978', '>0,<0', None)])

		db = open('test/snippet.json')
		result = get_vulnerabilities('ampache', db)
		db.close()
		self.assertEqual(result, \
			[('pyup.io-37866', '<3.6-alpha5', None), \
			('pyup.io-37865', '<3.8.0', 'CVE-2014-8620'), \
			('pyup.io-37864', '<3.8.2', None), \
			('pyup.io-37863', '<4.0.0', 'CVE-2019-12385, CVE-2019-12386')])


		name = str(uuid.uuid4())
		cve = str(uuid.uuid4())
		vid = str(uuid.uuid4())
		version = str(uuid.uuid4())
		db = io.StringIO('{ "%s": [ { "advisory": "test", "cve": "%s", "id": "%s", "v": "%s" } ] }' % (name, cve, vid, version))
		result = get_vulnerabilities(name, db)
		self.assertEqual(result, [(vid, version, cve)])
