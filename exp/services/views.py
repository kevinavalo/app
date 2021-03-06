from django.shortcuts import render

# Create your views here.
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
from elasticsearch import Elasticsearch
import operator
producer = KafkaProducer(bootstrap_servers='kafka:9092')
es = Elasticsearch(['es'])
# make a GET request and parse the returned JSON
# note, no timeouts, error handling or all the other things needed to do this for real
def getItemList(request):

    req = urllib.request.Request('http://models-api:8000/api/v1/item/get/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    return JsonResponse(resp)

def getItemDetail(request, id):
    if request.method == 'GET':
        
        auth = request.GET.get('auth')
        req_auth = urllib.request.Request('http://models-api:8000/api/v1/auth/getUserAuth/' + "?auth=" + auth)
        resp_json_auth = urllib.request.urlopen(req_auth).read().decode('utf-8')
        resp_auth = json.loads(resp_json_auth)

        req = urllib.request.Request('http://models-api:8000/api/v1/item/get/'+id+'/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        del resp['status']
        com = urllib.request.Request('http://models-api:8000/api/v1/comment/getList/item/'+id+'/')
        com_json =json.loads(urllib.request.urlopen(com).read().decode('utf-8'))

        if (resp_auth['status'] is True):
            recom_pair = { 'item_id': str(id), 'username': resp_auth['username']}
            print(recom_pair)
            producer.send('recommendation-topic', json.dumps(recom_pair).encode('utf-8'))
        final_resp = {'item':resp, 'comments':com_json}

        return JsonResponse(final_resp)

def getSortedListings(request):
    req = urllib.request.Request('http://models-api:8000/api/v1/item/get/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)['results']
    items = sorted(resp, key=lambda item: item['title'])

    items = json.dumps(items)
    return JsonResponse(items, safe=False)

@csrf_exempt
def comment(request):
    if request.method == 'POST':
        post_data = {'message': request.POST.get('message'),
                     'username':request.POST.get('username'),
                     'item': request.POST.get('item')}
        post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

        req = urllib.request.Request('http://models-api:8000/api/v1/comment/create/', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse(resp)
    return JsonResponse({'error':'could not comment'})
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
        if resp['response'] == 'username taken':
            return JsonResponse({'response':'username taken'})
        user = resp['response']
        auth_post_data = {'username':request.POST.get('username'), 'password':request.POST.get('password')}
        auth_post_encoded = urllib.parse.urlencode(auth_post_data).encode('utf-8')
        auth_req = urllib.request.Request('http://models-api:8000/api/v1/user/login/', data=auth_post_encoded, method='POST')
        resp_json = urllib.request.urlopen(auth_req).read().decode('utf-8')
        auth_resp = json.loads(resp_json)
        return JsonResponse({'user':resp,'auth':auth_resp, 'response': 'success'})

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
        auth = request.POST.get('auth')

        req_auth = urllib.request.Request('http://models-api:8000/api/v1/auth/getUserAuth/' + "?auth=" + auth)
        resp_json_auth = urllib.request.urlopen(req_auth).read().decode('utf-8')
        resp_auth = json.loads(resp_json_auth)

        if resp_auth['status']:
            post_data = {'title': request.POST.get('title'), 'description': request.POST.get('description'), 'price': request.POST.get('price'), 'category': request.POST.get('category'), 'owner': resp_auth['username']}
            post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

            req = urllib.request.Request('http://models-api:8000/api/v1/item/create/', data=post_encoded, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)

            item = resp['item-added']
            producer.send('new-listings-topic', json.dumps(item).encode('utf-8'))
            return JsonResponse({'item': item, 'status': True})
        elif resp_auth['response'] == 'Authenticator is expired':
            return JsonResponse({'status': False, 'response': 'Authenticator is expired'})
        else:
            return JsonResponse({'status': False})
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
                response.append(descending_users[i])
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

@csrf_exempt
def getProfile(request, id):
    if request.method == 'GET':
        req = urllib.request.Request('http://models-api:8000/api/v1/user/get/'+id+'/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        del resp['status']
        info = {}
        for key in resp:
            info = resp[key]
        return JsonResponse(info)

def searchItems(request):
    global es
    if request.method == 'GET':
        query = request.GET.get('query', '')
        try:
            resp = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
            items = []
            for resp in resp['hits']['hits']:
                items.append(resp['_source'])
            return JsonResponse({'status': 'success', 'items': items, 'itemsExist': True}, safe=False)
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e), 'itemsExist':False})
    else:
        return JsonResponse({'status': 'error, not a GET request'})


def getAuth(request):
    auth = request.GET.get('auth')
    req = urllib.request.Request('http://models-api:8000/api/v1/auth/getUserAuth/' + "?auth=" + auth)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    json_resp = json.loads(resp)
    return JsonResponse(json_resp['status'] == True, safe=False)

def getRecs(request, id):
    if request.method == 'GET':
        req = urllib.request.Request('http://models-api:8000/api/v1/rec/get/'+id+'/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse(resp)