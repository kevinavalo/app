from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.template import loader

LINK = "http://exp-api:8000/api/v1"
# Create your views here.

def itemDetail(request, id):
	req = urllib.request.Request('http://exp-api:8000/api/v1/getListings')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	itemList = resp['results']
	item = itemList[id]

	#return JsonResponse(item)
	return render(request, 'itemDetail.html', {'item': item})

def home(request):
	req = urllib.request.Request('http://exp-api:8000/api/v1/getSorted/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	# itemList = resp['results']
	# items = {}
	# for item in itemList:
	# 	items[item] = (itemList[item])

	return render(request, 'home.html', {'items':resp})
