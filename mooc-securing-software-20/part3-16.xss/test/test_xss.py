#!/usr/bin/env python3

import socket
import unittest
from tmc import points
from django.contrib.auth.models import User
from server.pages.models import Message, Mail


from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import json
from http.cookies import SimpleCookie

import time


@points('3.3.1', '3.3.2', '3.3.3', '3.3.4', '3.3.5')
class XssTest(LiveServerTestCase):

	# There is a 'feature' in selenium which may cause the firewall to react unless you provide an explicit port for the driver
	def free_port(self):
		free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		free_socket.bind(('localhost', 0))
		free_socket.listen(5)
		port = free_socket.getsockname()[1]
		free_socket.close()
		return port


	def test_xss(self):
		bob = User.objects.create_user(username='bob', password='squarepants')

		content = open('src/msg.html').read()

		msg = Message.objects.create(source=bob, target=bob, content=content)

		options = Options()
		options.headless = True
		options.add_argument('--no-sandbox')
		caps = webdriver.DesiredCapabilities.CHROME.copy()
		caps['goog:loggingPrefs'] = { 'browser':'ALL' }
		driver = webdriver.Chrome(port=self.free_port(), options=options, desired_capabilities=caps)
		driver.get(self.live_server_url + '/login/')

		username = driver.find_elements_by_name('username')[0]
		username.send_keys('bob')

		password = driver.find_elements_by_name('password')[0]
		password.send_keys('squarepants')

		driver.find_element_by_xpath("//button[@type='submit']").click()

		cookies = {c['name']: c['value'] for c in driver.get_cookies()}

		# just in case make sure that selenium has enough time to process the click.
		for i in range(20):
			if Mail.objects.count() >= 1:
				break
			time.sleep(0.1)

		log = '\n'.join([str(entry) for entry in driver.get_log('browser')])

		self.assertEqual(Mail.objects.count(), 1, msg='One mail message is expected\nBROWSER LOGS:\n'+log)

		m = Mail.objects.get()
		raw = json.loads(m.content)['content']
		stolen = SimpleCookie()
		stolen.load(raw)

		self.assertEqual(cookies['csrftoken'], stolen['csrftoken'].value, msg='\nBROWSER LOGS:\n'+log)
		self.assertEqual(cookies['sessionid'], stolen['sessionid'].value, msg='\nBROWSER LOGS:\n'+log)
