from django.shortcuts import render

# Create your views here.
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from datetime import datetime

# make a GET request and parse the returned JSON
# note, no timeouts, error handling or all the other things needed to do this for real
def getItemList(request):

    req = urllib.request.Request('http://models-api:8000/api/v1/item/get/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    return JsonResponse(resp)

def getSortedListings(request):
    req = urllib.request.Request('http://models-api:8000/api/v1/item/get/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)['results']
    items = sorted(resp, key=lambda item: item['title'])

    items = json.dumps(items)
    return JsonResponse(items, safe=False)

    # return JsonResponse(resp)
    # req = urllib.request.Request('http://models-api:8000/api/v1/item/get/')
    # resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    # itemList = resp_json['results']
    # return JsonResponse(json.load(itemList))
    # itemList = json.loads(itemList)
    # items = []
    # for item in itemList:
    #     items.append(item)
    # datetime.strptime(item['date_posted'], '%Y-%m-%d %H:%M:%S')
    # items = sorted(itemList, key=lambda item: datetime.strptime(item['date_posted'],  '%Y-%m-%d %H:%M:%S'))
    # return JsonResponse(json.loads(items))

