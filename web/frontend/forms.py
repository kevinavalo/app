from django import forms

class CreateListingForm(forms.Form):
	title = forms.CharField(max_length=50)

	choices = (('Furniture', 'Furniture'), ('Electronics', 'Electronics'), ('Bedroom', 'Bedroom'), ('Bath', 'Bath'))
	description = forms.CharField(max_length=200)
	price = forms.FloatField(required=True)
	category = forms.ChoiceField(required=False, choices=choices)