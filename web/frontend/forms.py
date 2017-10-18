from django import forms

class CreateListingForm(forms.Form):
	title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}))

	choices = (('Furniture', 'Furniture'), ('Electronics', 'Electronics'), ('Bedroom', 'Bedroom'), ('Bath', 'Bath'))
	description = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}))
	price = forms.FloatField(required=True, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Price'}))
	category = forms.ChoiceField(required=False, choices=choices, widget=forms.RadioSelect(attrs={'class':'form-control form-check-input', 'placeholder': 'Category'}))