#!/usr/bin/env python3

import os
import unittest
import socket
from unittest.mock import patch

from tmc.utils import load
from tmc import points

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class WaitForList(object):
	def __init__(self, count):
		self.count = count

	def __call__(self, driver):
		tasks = [li.text for li in driver.find_elements_by_xpath('/html/body/ul/li')]
		if len(tasks) >= self.count:
			return tasks
		else:
			return False

@points('2.1.1', '2.1.2', '2.1.3', '2.1.4', '2.1.5')
class TaskTest(LiveServerTestCase):

	modified_tasks = ['Find inner peace', 'Start a company']

	# There is a 'feature' in selenium which may cause the firewall to react unless you provide an explicit port for the driver
	def free_port(self):
		free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		free_socket.bind(('localhost', 0))
		free_socket.listen(5)
		port = free_socket.getsockname()[1]
		free_socket.close()
		return port

	def test_original(self):
		options = Options()
		options.headless = True
		options.add_argument('--no-sandbox')
		caps = webdriver.DesiredCapabilities.CHROME.copy()
		caps['goog:loggingPrefs'] = { 'browser':'ALL' }
		driver = webdriver.Chrome(port=self.free_port(), options=options, desired_capabilities=caps)
		driver.get(self.live_server_url)
		try:
			tasks = WebDriverWait(driver, 3).until(WaitForList(3))
		except TimeoutException:
			tasks = [li.text for li in driver.find_elements_by_xpath('/html/body/ul/li')]
		log = '\n'.join([str(entry) for entry in driver.get_log('browser')])
		self.assertEqual(tasks, ['Wash the car', 'Finish the project', 'Build a time machine'], msg='\nBROWSER LOGS:\n'+log)

	@patch('src.pages.views.tasks', modified_tasks)
	def test_modified(self):
		options = Options()
		options.headless = True
		options.add_argument('--no-sandbox')
		caps = webdriver.DesiredCapabilities.CHROME.copy()
		caps['goog:loggingPrefs'] = { 'browser':'ALL' }
		driver = webdriver.Chrome(port=self.free_port(), options=options, desired_capabilities=caps)
		driver.get(self.live_server_url)
		try:
			tasks = WebDriverWait(driver, 3).until(WaitForList(2))
		except TimeoutException:
			tasks = [li.text for li in driver.find_elements_by_xpath('/html/body/ul/li')]

		log = '\n'.join([str(entry) for entry in driver.get_log('browser')])
		self.assertEqual(tasks, self.modified_tasks, msg='\nBROWSER LOGS:\n'+log)
