# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from CommentManager.models import Comment

import json

# Create your tests here.

class CommentManagerTestCase(TestCase):

	fixtures = ["db.json"]

	def setup(self):
		pass

	def test_get_comment_success(self):
		comment = Comment.objects.get(id=1)
		url = self.client.get(reverse('getComment', args=[1]))
		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(response['response']['user'], comment.user.username)
		self.assertEquals(response['response']['item'], comment.item.title)
		self.assertEquals(response['response']['message'], comment.message)

	def test_get_comment_does_not_exist(self):
		url = self.client.get(reverse('getComment', args=[17]))

		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(response['response'], "no object found")

	def test_create_comment_success(self):
		preCommentTotalNum = len(Comment.objects.all())
		comment = {
			'username': 'kevinavalo',
			'item': 'Chair',
			'message': 'hello this is a new message'
		}

		url = self.client.post(reverse('createComment'), comment)

		response = json.loads(url.content.decode('utf-8'))

		postCommentTotalNum = len(Comment.objects.all())

		self.assertEquals(preCommentTotalNum, postCommentTotalNum-1)
		self.assertEquals(response['response']['status'], "success")

	def test_create_comment_message_failure(self):
		preCommentTotalNum = len(Comment.objects.all())
		comment = {
			'username': 'kevinavalo',
			'item': 'Chair',
		}

		url = self.client.post(reverse('createComment'), comment)

		response = json.loads(url.content.decode('utf-8'))

		postCommentTotalNum = len(Comment.objects.all())

		self.assertEquals(preCommentTotalNum, postCommentTotalNum)
		self.assertEquals(response['response'], "There needs to be a message")

	def test_create_comment_username_failure(self):
		preCommentTotalNum = len(Comment.objects.all())
		comment = {
			'item': 'Chair',
			'message': 'hello this is a new message',
		}

		url = self.client.post(reverse('createComment'), comment)

		response = json.loads(url.content.decode('utf-8'))

		postCommentTotalNum = len(Comment.objects.all())

		self.assertEquals(preCommentTotalNum, postCommentTotalNum)
		self.assertEquals(response['response'], "User does not exist, or you have entered an invalid username")

	def test_create_comment_item_failure(self):
		preCommentTotalNum = len(Comment.objects.all())
		comment = {
			'username': 'kevinavalo',
			'message': 'hello this is a new message',
		}

		url = self.client.post(reverse('createComment'), comment)

		response = json.loads(url.content.decode('utf-8'))

		postCommentTotalNum = len(Comment.objects.all())

		self.assertEquals(preCommentTotalNum, postCommentTotalNum)
		self.assertEquals(response['response'], "Item does not exit, or you have entered an invalid item name")

	def test_update_comment_success(self):
		comment = Comment.objects.get(id=1)

		oldMessage = comment.message
		newMessage = {'message': "hello this is a new message for this comment"}

		url = self.client.post(reverse('updateComment', args=[1]), newMessage)
		response = json.loads(url.content.decode('utf-8'))

		commentUpdatedMessage = Comment.objects.get(id=1).message

		self.assertEquals(newMessage['message'], commentUpdatedMessage)
		self.assertEquals(response['status'], 'success')
		self.assertEquals(response['response']['newMessage'], newMessage['message'])

	def test_update_comment_message_failure(self):
		comment = Comment.objects.get(id=1)

		oldMessage = comment.message
		newMessage = {}

		url = self.client.post(reverse('updateComment', args=[1]), newMessage)
		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(Comment.objects.get(id=1).message, oldMessage)
		self.assertEquals(response['response'], 'this is an invalid message')

	def test_delete_comment_success(self):
		preCommentNumber = len(Comment.objects.all())
		url = self.client.post(reverse('deleteComment', args=[1]), {})
		response = json.loads(url.content.decode('utf-8'))

		postCommentNumber = len(Comment.objects.all())
		self.assertEquals(response['status'], 'success')
		self.assertEquals(len(Comment.objects.all()), postCommentNumber)

	def test_delete_comment_failure(self):
		preCommentNumber = len(Comment.objects.all())
		url = self.client.post(reverse('deleteComment', args=[17]), {})
		response = json.loads(url.content.decode('utf-8'))

		postCommentNumber = len(Comment.objects.all())

		self.assertEquals(response['status'], 'error')
		self.assertEquals(response['response'], 'Comment was not found')
		self.assertEquals(preCommentNumber, postCommentNumber)

	def test_get_comment_list_success(self):
		comments = Comment.objects.all().filter(item=2)
		# comment_list = []
		# for comment in comments:
		# 			c = {
		# 				'message': comment.message,
		# 				'user': comment.user.username,
		# 				'date_posted': comment.date_posted
		# 			}
		# 			comment_list.append(c.copy())
		# comment_list_json = json.dumps(comment_list, sort_keys=True)	
		url = self.client.get(reverse('getCommentList', args=[2]))
		response = json.loads(url.content.decode('utf-8'))
		# responseList = json.dumps(response['response'], sort_keys=True)

		self.assertEquals(response['status'], 'success')
		# self.assertEquals(response['response'], comment_list_json)

	def test_get_comment_list_failure(self):
		url = self.client.get(reverse('getCommentList', args=[17]))
		response = json.loads(url.content.decode('utf-8'))

		self.assertEquals(response['status'], 'error')
		self.assertEquals(response['response'], 'There are no comments associated with this id.')