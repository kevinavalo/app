from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from . import forms
from django.http import JsonResponse
from django.template import loader

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