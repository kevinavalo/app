from django import forms
from django.core.validators import RegexValidator


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

class Registration(forms.Form):

    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    phone_number = forms.CharField(error_messages={'incomplete': 'Enter a phone number.'},
                             validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')],)
    city = forms.CharField(max_length=30)
    state = forms.CharField( widget=forms.Select(choices=STATE_CHOICES))

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(widget=forms.PasswordInput)

class CreateListingForm(forms.Form):
	title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}))

	choices = (('Bedframes & Headboards', 'Bedframes & Headboards'), ('Dressers & Nightstands', 'Dressers & Nightstands'), ('TV Room Furniture', 'TV Room Furniture'), ('Bathroom Furiture', 'Bathroom Furiture'), ('Dining Furniture', 'Dining Furniture'), ('Kitchen Accessories', 'Kitchen Accessories'), ('Couches & Chairs', 'Couches & Chairs'), ('Miscellaneous', 'Miscellaneous'))
	description = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))
	price = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Price'}))
	category = forms.ChoiceField(required=False, choices=choices, widget=forms.RadioSelect(attrs={'class':'form-control form-check-input', 'placeholder': 'Category'}))


class CommentForm(forms.Form):
	comment = forms.CharField(max_length=300, widget=forms.Textarea)