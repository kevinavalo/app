
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
# Create your models here.
class customer(models.Model):
	STATE_CHOICES = (
		('ALABAMA','AL'),
		('ALASKA','AK'),
		('ARIZONA','AZ'),
		('ARKANSAS','AR'),
		('CALIFORNIA','CA'),
		('COLORADO','CO'),
		('CONNECTICUT','CT'),
		('DELAWARE','DE'),
		('FLORIDA','FL'),
		('GEORGIA','GA'),
		('HAWAII','HI'),
		('IDAHO','ID'),
		('ILLINOIS','IL'),
		('INDIANA','IN'),
		('IOWA','IA'),
		('KANSAS','KS'),
		('KENTUCKY','KY'),
		('LOUISIANA','LA'),
		('MAINE','ME'),
		('MARYLAND','MD'),
		('MASSACHUSETTS','MA'),
		('MICHIGAN','MI'),
		('MINNESOTA','MN'),
		('MISSISSIPPI','MS'),
		('MISSOURI','MO'),
		('MONTANA','MT'),
		('NEBRASKA','NE'),
		('NEVADA','NV'),
		('NEW HAMPSHIRE','NH'),
		('NEW JERSEY','NJ'),
		('NEW MEXICO','NM'),
		('NEW YORK','NY'),
		('NORTH CAROLINA','NC'),
		('NORTH DAKOTA','ND'),
		('OHIO','OH'),
		('OKLAHOMA','OK'),
		('OREGON','OR'),
		('PENNSYLVANIA','PA'),
		('RHODE ISLAND','RI'),
		('SOUTH CAROLINA','SC'),
		('SOUTH DAKOTA','SD'),
		('TENNESSEE','TN'),
		('TEXAS','TX'),
		('UTAH','UT'),
		('VERMONT','VT'),
		('VIRGINIA','VA'),
		('WASHINGTON','WA'),
		('WEST VIRGINIA','WV'),
		('WISCONSIN','WI'),
		('WYOMING','WY')
		)
	# id = models.IntegerField(primary_key=True, default=None)
	username = models.CharField(max_length=30, unique=True, default=None)
	first_name = models.CharField(max_length=30, default=None)
	last_name = models.CharField(max_length=30, default=None)
	email = models.EmailField(default=None)
	password = models.CharField(max_length=30,default=None)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
	city = models.CharField(max_length=22)
	state = models.CharField(
    	max_length = 15,
    	choices = STATE_CHOICES,
    	)

class Authenticator(models.Model):
	user = models.ForeignKey(customer)
	authenticator = models.CharField(max_length=100, primary_key=True)
	timestamp = models.DateTimeField(default=timezone.now)
