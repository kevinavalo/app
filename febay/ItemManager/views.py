# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from datetime import date
from UserManager.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def getItemList(request):
    items = Item.objects.all()
    response = {}
    results = {}
    # response['status'] = request.status
    for item in items:
        results[item.pk] = {'title':item.title, 'description':item.description, 'price':item.price, 'date-posted': item.date_posted,
                             'category':item.category, 'owner':item.owner.username}
    response['status'] = 'success'
    response['results'] = results
    return JsonResponse(response)


def getItem(request, id):
    response = {}
    # response['status'] = request.status
    try:
        item = Item.objects.get(id = id)
        response[item.pk] = {'title': item.title, 'description': item.description, 'price':item.price, 'date-posted': item.date_posted,
                             'category': item.category, 'owner': item.owner.username}
        response['status'] = 'success'
    except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'response': 'no object found'})
    return JsonResponse(response)

@csrf_exempt
def create(request):
    response = {}
    # response['status'] = request.status
    if request.method == 'POST':
        try:
            date_posted = timezone.now()
            user = customer.objects.get(username = request.POST.get('owner'))
            item = Item.objects.create(
                title = request.POST.get('title'),
                description = request.POST.get('description'),
                category = request.POST.get('category'),
                price = request.POST.get('price'),
                owner = user,
                date_posted = date_posted
            )
            item.save()
            response['item-added'] = {'title':item.title, 'description':item.description, 'price':item.price, 'date-posted': item.date_posted,
                             'category':item.category, 'owner':item.owner.username}
            response['status'] = 'success'
        except():
            response['status'] = "error: Could not add item"

    return JsonResponse(response)

@csrf_exempt
def update(request, id):
    response = {}
    if request.method == "POST":
        try:
            item = Item.objects.get(id = id)
            if request.POST.get('title') != None:
                item.title = request.POST.get('title')
            if request.POST.get('description') != None:
                item.description = request.POST.get('description')
            if request.POST.get('category') != None:
                item.category = request.POST.get('category')
            if request.POST.get('price') != None:
                item.price = float(request.POST.get('price'))
            item.save()
            response['item-updated'] = {'title': item.title, 'description': item.description, 'price': item.price,
                                  'date-posted': item.date_posted, 'category': item.category, 'owner': item.owner.username}
            response['status'] = 'success'
        except():
            response['status'] = 'error: Could not update item'
    return JsonResponse(response)

@csrf_exempt
def delete(request, id):
    response = {}
    if request.method == 'POST':
        try:
            item = Item.objects.get(id=id)
            title = item.title
            item.delete()
            response['item-deleted'] = {'title': title}
            response['status'] = 'success'
        except():
            response['status'] = 'error: Could not delete item'

    return JsonResponse(response)