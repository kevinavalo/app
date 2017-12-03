# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone

from django.db import models
from UserManager.models import customer
from datetime import datetime

# Create your models here.
class Item(models.Model):
    owner = models.ForeignKey(customer)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    category = models.CharField(max_length=50)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Recommendation(models.Model):
	item_id = models.IntegerField(default=1)
	recommended_items = models.CharField(max_length=300,default='')
