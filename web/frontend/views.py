from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import ast
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .forms import *
from django.views.decorators.csrf import csrf_exempt

LINK = "http://exp-api:8000/api/v1"
# Create your views here.

def itemDetail(request, id):
	req = urllib.request.Request('http://exp-api:8000/api/v1/getListings')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	itemList = (resp['results'])
	item = {}
	for i in itemList:
		if (i['id']) == int(id):
		 	item = i
	#return JsonResponse(item)
	return render(request, 'itemDetail.html', {'item': item})

def home(request):
	req = urllib.request.Request('http://exp-api:8000/api/v1/getSorted/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	items = json.loads(resp)
	list = []

	# itemList = resp['results']
	# items = []
	# for item in resp:
	# 	items.append(item)

	return render(request, 'home.html', {'items':items})

def register(request):
	form = forms.Registration
	if request.method == 'POST':
		form = forms.Registration(request.POST)
		if form.is_valid():
			post_data = {'username':form.cleaned_data['username'],
						 'password':form.cleaned_data['password'],
						 'first_name':form.cleaned_data['first_name'],
						 'last_name':form.cleaned_data['last_name'],
						 'email':form.cleaned_data['email'],
						 'city':form.cleaned_data['city'],
						 'state':form.cleaned_data['state'],
						 'phone_number':form.cleaned_data['phone_number']}
			post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
			req = urllib.request.Request('http://exp-api:8000/api/v1/register/', data=post_encoded, method='POST')
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp_json)
			auth = resp['auth']['auth']
			response =  HttpResponseRedirect('/home')
			response.set_cookie("auth", auth)
			return response
		return render(request, 'register.html', {'form':form, 'message':form.errors})
	else:
		return render(request, 'register.html', {'form':form})

def login(request):
	login_form = LoginForm()
	if request.method == 'GET':
		return render(request, 'login.html',{'login_form':login_form})
	login_form = LoginForm(request.POST)
	if not login_form.is_valid():
		return render(request, 'login.html', {'login_form':login_form, 'message':login_form.errors})
	post_data = { 
		'username':login_form.cleaned_data['username'],
		'password':login_form.cleaned_data['password']}
	next = request.GET.get('next') or reverse('home')
	post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
	req = urllib.request.Request('http://exp-api:8000/api/v1/login/', data=post_encoded, method='POST')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if not resp or not resp['resp']:
		return render(request, 'login.html', {'login_form':login_form, 'message':'User could not be logged in'})
	auth = resp['resp']['auth']
	response = HttpResponseRedirect(next)
	response.set_cookie("auth", auth)
	return response

def logout(request):
	try:
		authenticator = request.COOKIES.get('auth')
		post_data = {
			'auth': authenticator}
		post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
		req = urllib.request.Request('http://exp-api:8000/api/v1/logout/', data=post_encoded, method='POST')
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp_json)
		response = HttpResponseRedirect('/home')
		response.delete_cookie('auth')
	except:
		return JsonResponse({'status': 'in except'})
	return response

@csrf_exempt
def createListing(request):

    # Try to get the authenticator cookie
    auth = request.COOKIES.get('auth')

    # If the authenticator cookie wasn't set...
    if not auth:
      # Handle user not logged in while trying to create a listing
     return HttpResponseRedirect(reverse("login") + "?next=" + reverse("createListing"))

    # If we received a GET request instead of a POST request...
    if request.method == 'GET':
        # Return to form page
        f = CreateListingForm()
        return render(request, 'createListing.html', {'form': f, 'created': False})

    # Otherwise, create a new form instance with our POST data
    f = CreateListingForm(request.POST)

    if request.method == 'POST':
	    if f.is_valid():
	    	post_data = {
	    		'title': f.cleaned_data['title'],
	    		'description': f.cleaned_data['description'],
	    		'price': f.cleaned_data['price'],
	    		'category': f.cleaned_data['category'],
	    		'auth': auth
	    	}

	    	post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

	    	req = urllib.request.Request('http://exp-api:8000/api/v1/createItem/', data=post_encoded, method='POST')
	    	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	    	resp = json.loads(resp_json)
	    	if not resp['status']:
	    		return HttpResponseRedirect(reverse("login") + "?next=" + reverse("createListing"))
	    	return JsonResponse({'status':'success', 'response': resp})
	    else:
	    	return JsonResponse({'status':'error', 'response':f.errors})
    # ...

    #WILL HAVE TO CHANGE THIS AFTER CREATING EXP API
    # Send validated information to our experience layer
    #resp = create_listing_exp_api(auth, ...)

    # Check if the experience layer said they gave us incorrect information
    #if resp and not resp['ok']:
        #if resp['error'] == exp_srvc_errors.E_UNKNOWN_AUTH:
            # Experience layer reports that the user had an invalid authenticator --
            #   treat like user not logged in
            #return HttpResponseRedirect(reverse("login") + "?next=" + reverse("createListing"))

    # ...
    return render(request, 'index.html')

def getPopularUsers(request):
	req = urllib.request.Request('http://exp-api:8000/api/v1/getPopularUsers/')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	users = json.loads(resp_json)

	return render(request, 'popularUsers.html', { 'users':users })

def getItemCategory(request):
	if request.method == 'GET':
		category = request.GET.get('category', '')
		data = {}
		data['category'] = category
		url_values = urllib.parse.urlencode(data)
		url = 'http://exp-api:8000/api/v1/getItemCategory/'
		full_url = url + '?' + url_values
		req = urllib.request.Request(full_url)
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		items = json.loads(resp_json)['items']

		return render(request, 'home.html', {'items': items})
	else:
		return home(request)