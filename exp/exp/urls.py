"""exp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from services import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
   	url(r'^api/v1/getListings/$', views.getItemList, name='itemList'),
    url(r'^api/v1/getSorted/$', views.getSortedListings, name='sortedList'),
    url(r'^api/v1/register/$', views.resgisterUser, name='register'),
    url(r'^api/v1/login/$', views.loginUser, name='login'),
    url(r'^api/v1/logout/$', views.logoutUser, name='logout'),
    url(r'^api/v1/createItem/$', views.createItem, name='createItem'),
    url(r'^api/v1/getPopularUsers/$', views.getPopularUsers, name='getPopularUsers'),
    url(r'^api/v1/getItemCategory/$', views.getItemCategory, name='getItemCategory'),
    url(r'^api/v1/getProfile/(?P<id>\d+)/$', views.getProfile, name='getProfile'),
    url(r'^api/v1/getItemDetail/(?P<id>\d+)/$', views.getItemDetail, name='getItemDetail'),
    url(r'^api/v1/comment/$', views.comment, name='comment'),
    url(r'^api/v1/searchItems/$', views.searchItems, name='searchItems'),
    url(r'^api/v1/getAuth/$', views.getAuth, name='getAuth'),
    url(r'^api/v1/getRecs/(?P<id>\d+)/$', views.getRecs, name='getRecommendations'),
]
