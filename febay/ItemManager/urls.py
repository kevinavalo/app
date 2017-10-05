from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^api/v1/item/get/$', getItemList),
    url(r'^api/v1/item/get/(?P<id>\d*)/$', getItem),
    url(r'^api/v1/item/create/', create),
    url(r'^api/v1/item/update/(?P<id>\d*)/$', update),
    url(r'^api/v1/item/delete/(?P<id>\d*)/$', delete),

]