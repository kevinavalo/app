from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^api/v1/user/register/$', views.register_user, name='registration'),
	url(r'^api/v1/user/get/(?P<id>\d*)/$', views.get_user, name='get_user'),
    url(r'^api/v1/user/get_users/$', views.get_users, name='get_users'),
    # url(r'^api/v1/user/login/$', views.login, name='login'),
    # url(r'^api/v1/user/logout/$', views.logout, name='logout'),
    url(r'^api/v1/user/delete_user/$', views.delete_user, name='delete_user'),
    url(r'^api/v1/user/update_user_email/$', views.update_user_email, name='update_user_email'),

]
