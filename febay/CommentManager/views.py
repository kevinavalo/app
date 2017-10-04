# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from CommentManager.models import Comment
from UserManager.models import customer
from ItemManager.models import Item
from django import forms
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

# Create your views here.

@csrf_exempt
def createComment(request):
	if request.method == 'POST':
		try:
			username = request.POST.get('username')
			user = customer.objects.get(username=username)
			if not user:
				return JsonResponse({'response': 'User must be authenticated to create comment'})

			itemTitle = request.POST.get('item')
			item = Item.objects.get(title=itemTitle)
			if not item:
				return JsonResponse({'response': 'Comments must be associated with an item'})

			message = request.POST.get('message')
			if not message:
				return JsonResponse({'response': 'There needs to be a message'})

			comment = Comment.objects.create(user=user, item=item, message=message)
			comment.save()
			response = {'status': 'success', 'username': comment.user.username, 'item': comment.item.title, 'message': comment.message}
			return JsonResponse({'response': response})
		except Exception as e:
			return JsonResponse({'response': str(e)})
	else:
		return JsonResponse({'status': 'error', 'response': 'Not a POST method'})

def getComment(request, pk):
	if request.method == 'GET':
		id = pk
		if id:
			try:
				comment = Comment.objects.get(id=id)
				response = {
					"user": comment.user.username,
					"item": comment.item.title,
					"message": comment.message,
					"date_posted": comment.date_posted
				}
				return JsonResponse({'status': 'success', 'response': response})
			except ObjectDoesNotExist:
				return JsonResponse({'status': 'error', 'response': 'no object found'})
		else:
			return JsonResponse({'status': 'error', 'response': 'Comment not found'})
	else:
		return JsonResponse({'status': 'error', 'response': 'Not a GET method'})

@csrf_exempt
def updateComment(request, pk):
	if request.method == 'POST':
		id = pk
		if id:
			try:
				newMessage = request.POST.get('message', False)
				if not newMessage:
					return JsonResponse({'response': 'this is an invalid message'})
				comment = Comment.objects.get(id=id)
				comment.message = newMessage
				comment.save()
				response = {'newMessage': comment.message, 'user': comment.user.username, 'item': comment.item.title}
				return JsonResponse({'status': 'success', 'response': response})
			except:
				return JsonResponse({'status': 'error', 'response': 'Comment was not updated'})
		else:
			return JsonResponse({'status': 'error', 'response': 'Comment not found'})
	else:
		return JsonResponse({'status': 'error', 'response': 'Not a POST method'})

@csrf_exempt
def deleteComment(request, pk):
	if request.method == 'POST':
		id = pk
		if id:
			try:
				response = Comment.objects.get(id=id).delete()
				return JsonResponse({'status': 'success', 'response': 'Successfully deleted message'})
			except ObjectDoesNotExist:
				return JsonResponse({'status': 'error', 'response': 'Comment was not found'})
		else:
			return JsonResponse({'status': 'error', 'response': 'Comment id does not exist'})
	else:
		return JsonResponse({'status': 'error', 'response': 'Not a POST method'})

@csrf_exempt
def getCommentList(request, pk):
	if request.method == 'GET':
		id = pk
		comment_list = []
		if id:
			try:
				comments = Comment.objects.all().filter(item=id)
				if not comments:
					return JsonResponse({'status': 'error', 'response': 'There are no comments associated with this id.'})
				for comment in comments:
					c = {
						'message': comment.message,
						'user': comment.user.username,
						'date_posted': comment.date_posted
					}
					comment_list.append(c.copy())
				return JsonResponse({'status': 'success', 'response': comment_list})
			except Exception as e:
				return JsonResponse({'status': 'error', 'response': str(e)})
		else:
			return JsonResponse({'status': 'error', 'response': 'Error finding comments related to item id'})
	else:
		return JsonResponse({'status': 'error', 'response': 'Not a GET method'})

