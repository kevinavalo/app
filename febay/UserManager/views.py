# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import User, customer
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def register_user(request):
	if request.method == 'POST':
		user = customer.objects.create_user(
			first_name = request.POST.get('first_name'),
			last_name = request.POST.get('last_name'),
			username = request.POST.get('username'),
			email = request.POST.get('email'),
			city = request.POST.get('city'),
			state = request.POST.get('state'),
			phone_number = request.POST.get('phone_number'),
			password = request.POST.get('password')
			)
		return JsonResponse({'status': 'success', 'Response':{'first name': user.first_name,'last name': user.last_name, 'username': user.username, 'email': user.email, 'state':user.state, 'city':user.city, 'phone number': user.phone_number,'id':user.id}})
	else:
		return JsonResponse({'status': 'error', 'Response': 'Could not register user'})

@csrf_exempt
def get_user(request,id):
	response = {}
	if request.method == 'GET':
		try:
			user = customer.objects.get(id = id)
			response[user.username] = {'first name': user.first_name,'last name': user.last_name, 
			'username': user.username, 'email': user.email, 'state':user.state, 
			'city':user.city, 'phone number': user.phone_number,'id':user.id}
			response['status'] = 'success'
		except ObjectDoesNotExist:
			response['status'] = 'error: user does not exist'
	return JsonResponse(response)

@csrf_exempt
def get_users(request):
    users = customer.objects.all().values('username','first_name', 'last_name')  # or simply .values() to get all fields
    users_list = list(users)  # important: convert the QuerySet to a list object
    status = {'status': 'success'}
    users_list.append(status)
    return JsonResponse(users_list, safe=False)

# @csrf_exempt
# def login(request):
# 	status = {}
# 	if request.method == 'POST':
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')
# 		user = authenticate(username=username, password=password)
# 		if user is not None:
# 			if user.is_active:
# 				auth_login(request, user)
# 				status = {'status': 'successful login'}
# 			else:
# 				status = {'status': 'inactive user'}
# 		else:
# 			status = {'status': 'user not found'}
# 	return JsonResponse({'response':status})

# @csrf_exempt
# def logout(request):
# 	status = {}
# 	if request.method == 'POST':
# 		username = request.POST.get('username')
# 		auth_logout(customer.objects.get(username = username))
# 		status = {'status': 'sucessfully logged out'}
# 	return JsonResponse({'response':status})


@csrf_exempt
def delete_user(request):
	status = {}
	if request.method == 'POST':
		username = request.POST.get('username')
		u = customer.objects.get(username = username)
		if u is not None:
			u.delete()
			status = {'status': 'sucessfully deleted user'}
		else:
			status = {'status': 'user not found'}
	else:
		status = {'status': 'unsuccessful deletion of user'}
	return JsonResponse({'response':status})

@csrf_exempt
def update_user_email(request):
	status = {}
	response = {}
	if request.method == 'POST':
		username = request.POST.get('username')
		new_email = request.POST.get('new_email')
		user = customer.objects.get(username = username)
		user.email = new_email
		user.save()
		response = {'first name': user.first_name,'last name': user.last_name, 
			'username': user.username, 'email': user.email, 'state':user.state, 
			'city':user.city, 'phone number': user.phone_number,'id':user.id}
		status = {'status': 'success'}
	else:
		status = {'status': 'error updating user email'}
	return JsonResponse({'status': status, 'response':response})
    	

