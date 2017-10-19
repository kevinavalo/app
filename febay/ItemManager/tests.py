# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
import json

# Create your tests here.

class Tests(TestCase):

    fixtures = ['db.json']

    def testGetListItemPass(self):
        c = Client()
        resp = c.get('/api/v1/item/get/')
        items = resp.json()
        self.assertEqual(items['count'], 4)

    def testGetFirstItemPass(self):
        c = Client()
        resp_json = c.get('/api/v1/item/get/1/')
        item = resp_json.json()
        # item = item['results']['1']
        self.assertEqual(item['1']['price'], 5.99)
        self.assertEqual(item['1']['title'], 'Desk')

    def testGetFirstItemFail(self):
        c = Client()
        resp_json = c.get('/api/v1/item/get/90/')
        status = json.loads(resp_json.content.decode('utf-8'))['status']
        self.assertEqual(status, 'Item matching query does not exist.')

    def testUpdateItemPass(self):
        c = Client()
        resp_json = c.post('/api/v1/item/update/2/', {'title':'Trash Can'})
        status = resp_json.status_code
        self.assertEqual(status, 200)
        item_json = c.get('/api/v1/item/get/2/')
        item = item_json.json()
        self.assertEqual(item['2']['title'], 'Trash Can')

    def testUpdateItemFail(self):
        c = Client()
        resp_json = c.post('/api/v1/item/update/90/', {'title':'Trash Can'})
        status = json.loads(resp_json.content.decode('utf-8'))['status']
        self.assertEqual(status,'Item matching query does not exist.' )

    def testUpdateItemFail2(self):
        c = Client()
        item = c.get('/api/v1/item/get/1/').json()['1']
        resp_json = c.post('/api/v1/item/update/1/', {'name': 'Trash Can'})
        new_item = json.loads(resp_json.content.decode('utf-8'))['item-updated']
        self.assertEqual(item, new_item)

    def testCreateItemPass(self):
        c = Client()
        count = c.get('/api/v1/item/get/').json()['count']

        resp = c.post('/api/v1/item/create/',{'owner':'kev','title':'Bed Frame',
                                              'description':'cheap!','category':'bedroom',
                                              'price':'10'})
        new_count = c.get('/api/v1/item/get/').json()['count']

        status = resp.status_code
        self.assertEqual(status, 200)
        self.assertEqual(count+1, new_count)

    def testCreateItemFail(self):
        c = Client()
        resp = c.post('/api/v1/item/create/',{'owner':'kat',
                                              'description':'cheap!','category':'bedroom',
                                              'price':'10'})
        status = json.loads(resp.content.decode())
        self.assertEqual(status['status'], '(1048, "Column \'title\' cannot be null")')

    def testDeleteItemPass(self):
        c = Client()
        count = c.get('/api/v1/item/get/').json()['count']
        resp = c.post('/api/v1/item/delete/1/', {})
        status = json.loads(resp.content.decode('utf-8'))['status']
        new_count = c.get('/api/v1/item/get/').json()['count']
        self.assertEqual(status,'success' )
        self.assertEqual(count-1, new_count)

    def testDeleteItemFail(self):
        c = Client()
        count = c.get('/api/v1/item/get/').json()['count']
        resp = c.post('/api/v1/item/delete/36/', {})
        status = json.loads(resp.content.decode('utf-8'))['status']
        new_count = c.get('/api/v1/item/get/').json()['count']
        self.assertEqual(status,'Item matching query does not exist.' )
        self.assertEqual(count, new_count)

