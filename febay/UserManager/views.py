# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import customer, Authenticator
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import hashers
import os
import hmac
from febay import settings
from django.forms.models import model_to_dict
from datetime import datetime, timedelta
from django.utils import timezone
# import django settings file

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            user = customer.objects.create(
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                username = request.POST.get('username'),
                email = request.POST.get('email'),
                city = request.POST.get('city'),
                state = request.POST.get('state'),
                phone_number = request.POST.get('phone_number'),
                password = hashers.make_password(request.POST.get('password'))
                )
            user.save()
        except Exception as e:
            return JsonResponse({'status': str(e)})
        return JsonResponse({'status': 'success', 'response':{'first name': user.first_name,'last name': user.last_name, 'username': user.username, 'email': user.email, 'state':user.state, 'city':user.city, 'phone number': user.phone_number,'id':user.id}})
    else:
        return JsonResponse({'status': 'error', 'response': 'Could not register user'})

@csrf_exempt
def get_user(request,id):
    response = {}
    if request.method == 'GET':
        try:
            user = customer.objects.get(id = id)
            response[user.username] = {'first_name': user.first_name,'last_name': user.last_name,
            'username': user.username, 'email': user.email, 'state':user.state,
            'city':user.city, 'phone_number': user.phone_number,'id':user.id}
            response['status'] = 'success'
        except ObjectDoesNotExist:
            response['status'] = 'error: user does not exist'
    return JsonResponse(response)

@csrf_exempt
def get_users(request):
    users = customer.objects.all().values('username','first_name', 'last_name','id')  # or simply .values() to get all fields
    users_list = list(users)  # important: convert the QuerySet to a list object
    status = {'status': 'success'}
    response = {}
    response['users_list'] = users_list
    response['status'] = status
    return JsonResponse(response, safe=False)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = customer.objects.get(username=username)
            if hashers.check_password(password, user.password):
                create_auth(request)
                auth = (Authenticator.objects.get(user=user))

                return JsonResponse({'status': 'success','auth':auth.authenticator},safe=False)
            else:
                return JsonResponse({'status': 'error','response':'Incorrect Password'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error','response':'User does not exist'})
    return JsonResponse({'status': 'error','response':'POST expected, GET found'})


# @csrf_exempt
# def logout(request):
# 	if request.method == 'POST':
# 		delete_auth_resp = delete_auth(request, request.POST.get('auth'))
# 		return delete_auth_resp
# 	return JsonResponse({'response':'didn\'t work'})


@csrf_exempt
def delete_user(request):
    status = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            u = customer.objects.get(username = username)
        except ObjectDoesNotExist:
            return JsonResponse({'response': {'status': 'user not found'}})
        if u is not None:
            u.delete()
            status = {'status': 'successfully deleted user'}
        else:
            status = {'status': 'user not found'}
    else:
        status = {'status': 'unsuccessful deletion of user'}
    return JsonResponse({'response':status})

@csrf_exempt
def update_user(request, id):
    status = {}
    response = {}
    if request.method == 'POST':
        try:
            try:
                user = customer.objects.get(id = id)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error: user does not exist'})
            if request.POST.get('new_email') != None:
                user.email = request.POST.get('new_email')
            if request.POST.get('new_password') != None and request.POST.get('password_confirmation') != None and request.POST.get('new_password') == request.POST.get('password_confirmation'):
                user.password = request.POST.get('new_password')
            if request.POST.get('new_phone_number') != None:
                user.phone_number = request.POST.get('new_phone_number')
            if request.POST.get('new_state') != None:
                user.state = request.POST.get('new_state')
            if request.POST.get('new_city') != None:
                user.city = request.POST.get('new_city')
            user.save()
            response = {'first name': user.first_name,'last name': user.last_name,
                'username': user.username, 'email': user.email, 'state':user.state,
                'city':user.city, 'phone number': user.phone_number,'id':user.id}
            status = {'status': 'success'}
        except():
            status = {'status': 'error: could not update user'}
    else:
        status = {'status': 'error: could not update user'}
    return JsonResponse({'status': status, 'response':response})

@csrf_exempt
def create_auth(request):
    if request.method == 'POST':
        authenticator = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        try:
            user = customer.objects.get(username=request.POST.get('username'))
            auth = Authenticator(
                user = user,
                authenticator = authenticator,
            )
            auth.save()
            return JsonResponse({'status':'success', 'user':auth.user.username, 'auth':auth.authenticator,
                                 'timestamp':auth.timestamp})
        except Exception as e:
            return JsonResponse({'status': str(e)})

    return JsonResponse({'status': 'Error, must make POST request'})

@csrf_exempt
def delete_auth(request):
    if request.method == 'POST':
        try:
            del_auth = Authenticator.objects.get(authenticator=request.POST.get('auth'))
            response = {'user': del_auth.user.username, 'auth':del_auth.authenticator, 'status': 'logged out'}
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'Error, auth doesn\'t exist'})

        del_auth.delete()
        return JsonResponse({'status':'success', 'response': response})
    return JsonResponse({'status': 'Error, must make POST request'})

@csrf_exempt
def get_auth(request):
    auth_models = Authenticator.objects.all()
    json = list(map(model_to_dict, auth_models))
    return JsonResponse(json, safe=False)

def get_user_auth(request):
	if request.method == 'GET':
		try:
			auth = Authenticator.objects.get(authenticator=request.GET.get('auth'))
		except ObjectDoesNotExist:
			return JsonResponse({'status': False})
		username = auth.user.username
		timestamp = auth.timestamp
		if (timezone.now() - timestamp) < timedelta(1):
			auth.delete()
			return JsonResponse({'status': False, 'response': 'Authenticator is expired'}, safe=False)
		response = {'username': username, 'status': True, 'auth': auth.authenticator, 'timestamp': auth.timestamp}
		return JsonResponse(response, safe=False)
	else:
		return JsonResponse({'status': 'error'})