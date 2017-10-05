from django.shortcuts import render

# Create your views here.
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse

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
    itemList = resp_json['results']
    items = {}
    for item in itemList:
        items[item] = (itemList[item])

    items = sorted(items, key=items['date_posted'])
    return items
