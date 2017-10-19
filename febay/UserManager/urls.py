from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^api/v1/user/register/$', views.register_user, name='registration'),
	url(r'^api/v1/user/get/(?P<id>\d*)/$', views.get_user, name='get_user'),
    url(r'^api/v1/user/get_users/$', views.get_users, name='get_users'),
    url(r'^api/v1/user/login/$', views.login, name='login'),
    # url(r'^api/v1/user/logout/$', views.logout, name='logout'),
    url(r'^api/v1/user/delete_user/$', views.delete_user, name='delete_user'),
    url(r'^api/v1/user/update/(?P<id>\d*)/$', views.update_user, name='update_user'),
    url(r'^api/v1/auth/create/$', views.create_auth, name='create_auth'),
    url(r'^api/v1/auth/get/$', views.get_auth, name='get_auths'),
    url(r'^api/v1/auth/delete/$', views.delete_auth, name='delete_auth'),
    url(r'^api/v1/auth/getUserAuth/$', views.get_user_auth, name='getUserAuth')

]
