from django.shortcuts import render

# Create your views here.
import urllib.request
import urllib.parse
import json

# make a GET request and parse the returned JSON
# note, no timeouts, error handling or all the other things needed to do this for real
def home(request):
    print ("About to perform the GET request...")

    req = urllib.request.Request('/api/v1/item/get/')

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    print(resp)
    return render(request, 'index.html')

    # make a POST request.
    # we urlencode the dictionary of values we're passing up and then make the POST request
    # again, no error handling

    # print ("About to perform the POST request...")
    #
    # post_data = {'title': 'Demo Post', 'body': 'This is a test', 'userId': 1}
    #
    # post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    #
    # req = urllib.request.Request('http://placeholder.com/v1/api/posts/create', data=post_encoded, method='POST')
    # resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    #
    # resp = json.loads(resp_json)
    # print(resp)