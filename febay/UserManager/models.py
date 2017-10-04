
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class customer(User):
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

	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
	city = models.CharField(max_length=22)
	state = models.CharField(
    	max_length = 15,
    	choices = STATE_CHOICES,
    	)


