# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import User, customer
from django.urls import reverse

import json

# Create your tests here.

class UserManagerTestCase(TestCase):

	fixtures = ["db.json"]

	def setup(self):
		pass

	def test_register_user_success(self):
		newUser = {
			'first_name': 'test',
			'last_name': 'user',
			'username': 'testuser',
			'email': 'test@gmail.com',
			'city': 'Charlottesville',
			'state': 'VA',
			'phone_number': '1234567890',
			'password': 'password'
		}

		preUserTotal = len(customer.objects.all())
		url = self.client.post(reverse('registration'), newUser)
		postUserTotal = len(customer.objects.all())

		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(response['status'], 'success')
		self.assertEquals(response['Response']['first name'], newUser['first_name'])
		self.assertEquals(preUserTotal, postUserTotal-1)


	def test_register_user_failure(self):
		newUser = {
			'first_name': 'test',
			'last_name': 'user',
			'email': 'test@gmail.com',
			'city': 'Charlottesville',
			'state': 'VA',
			'phone_number': '1234567890',
			'password': 'password'
		}

		preUserTotal = len(customer.objects.all())
		url = self.client.post(reverse('registration'), newUser)
		postUserTotal = len(customer.objects.all())

		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(response['status'], 'error')
		self.assertEquals(response['Response'], 'There was an error creating the user, invalid input')
		self.assertEquals(preUserTotal, postUserTotal)

	def test_get_user_success(self):
		user = customer.objects.get(id=1)

		url = self.client.get(reverse('get_user', args=[1]))
		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(response['status'], 'success')
		self.assertEquals(response[user.username]['first name'], user.first_name)
		self.assertEquals(response[user.username]['username'], user.username)

	def test_get_user_failure(self):
		url = self.client.get(reverse('get_user', args=[18]))
		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(response['status'], 'error: user does not exist')

	def test_get_users_success(self):
		url = self.client.get(reverse('get_users'))
		response = json.loads(url.content.decode('utf-8'))

		users = customer.objects.all().values('username', 'first_name', 'last_name')
		users_list = list(users)

		self.assertEquals(users_list[1]['username'], response[1]['username'])
		self.assertEquals(len(users_list), len(response)-1)

	def test_get_users_empty_list(self):
		customer.objects.all().delete()

		url = self.client.get(reverse('get_users'))
		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(0, len(response)-1)

	def test_delete_user_success(self):
		url = self.client.post(reverse('delete_user'), {'username': 'kevinavalo'})
		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(response['response']['status'], 'successfully deleted user')