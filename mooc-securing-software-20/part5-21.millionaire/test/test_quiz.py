#!/usr/bin/env python3

import os
import unittest
from tmc import points

from django.test import TestCase


@points('5.2.1', '5.2.2', '5.2.3', '5.2.4', '5.2.5')
class QuizTest(TestCase):

	def test_normal(self):
		response = self.client.get('/', follow=True)
		response = self.client.get('/topic/1', follow=True)
		response = self.client.get('/quiz/1', follow=True)
		response = self.client.get('/quiz/1/0', follow=True)
		response = self.client.get('/quiz/1/1', follow=True)
		self.assertContains(response, 'Awesome! You beat the game!', msg_prefix='Answering questions correctly does not work')

	def test_change(self):
		response = self.client.get('/', follow=True)
		response = self.client.get('/topic/1', follow=True)
		response = self.client.get('/quiz/1', follow=True)
		response = self.client.get('/quiz/1/0', follow=True)
		response = self.client.get('/quiz/2/2', follow=True)
		self.assertContains(response, 'We suspect that you are trying to cheat in the game', msg_prefix='Topics can be changed mid quiz')

	def test_backtrack(self):
		response = self.client.get('/', follow=True)
		response = self.client.get('/topic/1', follow=True)
		response = self.client.get('/quiz/1', follow=True)
		response = self.client.get('/quiz/1/1', follow=True)
		response = self.client.get('/quiz/1/0', follow=True)
		self.assertContains(response, 'We suspect that you are trying to cheat in the game', msg_prefix='Can backtrack with wrong question')

	def test_finish(self):
		response = self.client.get('/finish/', follow=True)
		self.assertContains(response, 'We suspect that you are trying to cheat in the game', msg_prefix='Finish page is reachable immediately')
