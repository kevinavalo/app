from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from . import forms
from django.http import JsonResponse
from django.template import loader
from django.http import HttpResponseRedirect

LINK = "http://exp-api:8000/api/v1"
# Create your views here.

def itemDetail(request, id):
	req = urllib.request.Request('http://exp-api:8000/api/v1/getListings')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	itemList = (resp['results'])
	item = {}
	for i in itemList:
		if (i['id']) == int(id):
		 	item = i
	#return JsonResponse(item)
	return render(request, 'itemDetail.html', {'item': item})

def home(request):
	req = urllib.request.Request('http://exp-api:8000/api/v1/getSorted/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	items = json.loads(resp)
	list = []

	# itemList = resp['results']
	# items = []
	# for item in resp:
	# 	items.append(item)

	return render(request, 'home.html', {'items':items})


def register(request):
	form = forms.Registration
	if request.method == 'POST':
		form = forms.Registration(request.POST)
		if form.is_valid():
			post_data = {'username':form.cleaned_data['username'],
						 'password':form.cleaned_data['password'],
						 'first_name':form.cleaned_data['first_name'],
						 'last_name':form.cleaned_data['last_name'],
						 'email':form.cleaned_data['email'],
						 'city':form.cleaned_data['city'],
						 'state':form.cleaned_data['state'],
						 'phone_number':form.cleaned_data['phone_number']}
			post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
			req = urllib.request.Request('http://exp-api:8000/api/v1/register/', data=post_encoded, method='POST')
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			return JsonResponse({'status':'success','response':resp})
		return render(request, 'register.html', {'form':form, 'message':form.errors})
	else:
		return render(request, 'register.html', {'form':form})


def login(request):
	login_form = forms.LoginForm
	if request.method == 'GET':
		return render(request, 'login.html',{'login_form':login_form})
	login_form = forms.LoginForm(request.POST)
	if not login_form.is_valid():
		return render(request, 'login.html', {'login_form':login_form, 'message':login_form.errors})
	post_data = { 
		'username':login_form.cleaned_data['username'],
		'password':login_form.cleaned_data['password']}
	post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/api/v1/login/', data=post_encoded, method='POST')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if not resp or not resp['resp']:
		return render(request, 'login.html', {'login_form':login_form, 'message':'User could not be logged in'})
	auth = resp['resp']['auth']
	response = HttpResponseRedirect('/home')
	response.set_cookie("auth", auth)
	return response

def logout(request):
	req = urllib.request.Request('http://exp-api:8000/api/v1/logout/', method='POST')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	response = HttpResponseRedirect('/home')
	response.delete_cookie("auth")
	return response