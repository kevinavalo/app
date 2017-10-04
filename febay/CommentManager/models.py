# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from UserManager.models import customer
from ItemManager.models import Item


# Create your models here.

class Comment(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(customer)
	item = models.ForeignKey(Item)
	message = models.CharField(max_length=200)
	date_posted = models.DateTimeField(default=timezone.now)
