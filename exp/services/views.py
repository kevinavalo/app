from django.shortcuts import render

# Create your views here.
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
import operator

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
@csrf_exempt
def resgisterUser(request):
    if request.method == 'POST':
        post_data = {'username': request.POST.get('username'),
                     'password':request.POST.get('password'),
                     'email':request.POST.get('email'),
                     'first_name':request.POST.get('first_name'),
                     'last_name':request.POST.get('last_name'),
                     'city':request.POST.get('city'),
                     'state':request.POST.get('state'),
                     'phone_number':request.POST.get('phone_number')}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

        req = urllib.request.Request('http://models-api:8000/api/v1/user/register/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        user = resp['response']
        auth_post_data = {'username':user['username'], 'password':request.POST.get('password')}
        auth_post_encoded = urllib.parse.urlencode(auth_post_data).encode('utf-8')
        auth_req = urllib.request.Request('http://models-api:8000/api/v1/user/login/', data=auth_post_encoded, method='POST')
        resp_json = urllib.request.urlopen(auth_req).read().decode('utf-8')
        auth_resp = json.loads(resp_json)
        return JsonResponse({'user':resp,'auth':auth_resp})

@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        post_data = {'username': request.POST.get('username'),
                     'password':request.POST.get('password')}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/user/login/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse({'resp':resp})

@csrf_exempt
def logoutUser(request):
    if request.method == 'POST':
        post_data = {'auth': request.POST.get('auth')}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/api/v1/auth/delete/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse({'resp':resp})


@csrf_exempt
def createItem(request):
    if request.method == 'POST':
        post_data = {'title': request.POST.get('title'), 'description': request.POST.get('description'), 'price': request.POST.get('price'), 'category': request.POST.get('category'), 'auth': request.POST.get('auth')}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

        req = urllib.request.Request('http://models-api:8000/api/v1/item/create/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        item = resp['item-added']
        return JsonResponse({'item': item})
    return JsonResponse({'status': 'error'})

#get popular users based on number of items they have listed
def getPopularUsers(request):
    if request.method == 'GET':
        req = urllib.request.Request('http://models-api:8000/api/v1/user/get_users/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        users_list = json.loads(resp_json)['users_list']

        req_item = urllib.request.Request('http://models-api:8000/api/v1/item/get/')
        resp_item_json = urllib.request.urlopen(req_item).read().decode('utf-8')
        items_list = json.loads(resp_item_json)['results']

        total_count = {}
        descending_users = []
        response = []
        for user in users_list:
            total_count[user['username']] = 0

        for user in users_list:
            for item in items_list:
                if item['owner'] == user['username']:
                    total_count[item['owner']] += 1

        d = sorted(total_count.items(), key=operator.itemgetter(1), reverse=True)

        for tup in d:
            for user in users_list:
                if user['username'] == tup[0]:
                    descending_users.append(user)

        if len(descending_users) > 5:
            for i in range(0,4):
                response.append(descending_users.get(i))
        else:
            response = descending_users
        return JsonResponse(response, safe=False)
    return JsonResponse({'status': 'error'})

def getItemCategory(request):
    if request.method == 'GET':
        category = request.GET.get('category', '')
        if category != '':
            req = urllib.request.Request('http://models-api:8000/api/v1/item/get/')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)['results']

            items = []
            for item in resp:
                if item['category'] == category:
                    items.append(item)

            return JsonResponse({'items': items, 'status': 'success'}, safe=False)
        else: 
            return JsonResponse({'status': 'error this is not a valid category'})
    else:
        return JsonResponse({'status': 'error, this is not a GET method'})