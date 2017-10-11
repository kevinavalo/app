from django import forms

class Registration(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    phone = forms.IntegerField()
    city = forms.CharField(max_length=30)
    state = forms.CharField(max_length=2)

