# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import User, customer

class UpdateProfile(TestCase):
	#setUp method is called before each test in this class
	def setUp(self):
		self.user = customer.objects.create_user(
			first_name = 'Jane',
			last_name = 'Doe',
			username = 'janedoe123',
			email = 'jane@doe.com',
			city = 'South Orange',
			state = 'NEW JERSEY',
			phone_number = +19739021648,
			password = 'helloworld'
			)
		pass #nothing to set up


    # def success_update_password(self):
    # 	#assumes user with id 1 is stored in db
    # 	response = self.client.get(reverse('all_orders_list', kwargs={'user_id':1}))

    # 	#checks that response contains parameter order list & implicitly
    # 	# checks that the HTTP status code is 200
    # 	self.assertContains(response, 'order_list')
    # 	#user_id not given in url, so error

    def success_update_email(self):
    	self.user.email = 'doe@jane.com'
    	self.assertEquals(self.user.email, 'doe@jane.com')
    	self.user.email = 'jane@doe.com'

    def invalid_update_email(self):
    	self.user.email = 'doejane.com'
    	self.assertEquals(self.user.email, 'jane@doe.com')

    def success_update_state(self):
    	self.user.state = 'CALIFORNIA'
    	self.assertEquals(self.user.state, 'CALIFORNIA')

    def success_update_city(self):
    	self.user.city = 'Maplewood'
    	self.assertEquals(self.user.state, 'Maplewood')

    def success_update_phone_number(self):
    	self.user.phone_number = +1234567891
    	self.assertEquals(self.user.phone_number, +1234567891)
    	self.user.phone_number = +19739021648

    def invalid_update_phone_number(self):
    	self.user.phone_number = 1
    	self.assertEquals(self.user.phone_number, +19739021648)

    def success_update_first_name(self):
    	self.user.first_name = 'John'
    	self.assertEquals(self.user.first_name, 'John')

    def success_update_last_name(self):
    	self.user.last_name = 'Dow'
    	self.assertEquals(self.user.last_name, 'Dow')

    # def fails_invalid(self):
    # 	response = self.client.get(reverse('all_orders_list'))
    # 	self.assertEquals(response.status_code, 404)
    # 	#tearDown method is called after each test

    def tearDown(self):
    	self.user.delete()
    	pass #nothing to tear down