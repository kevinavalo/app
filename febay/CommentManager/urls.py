from django.conf.urls import url, include
from CommentManager import views

urlpatterns = [
	url(r'^api/v1/comment/create/$', views.createComment, name='createComment'),
	url(r'^api/v1/comment/get/(?P<pk>\d+)/$', views.getComment, name='getComment'),
	url(r'^api/v1/comment/update/(?P<pk>\d+)/$', views.updateComment, name='updateComment'),
	url(r'^api/v1/comment/delete/(?P<pk>\d+)/$', views.deleteComment, name='deleteComment'),
	url(r'^api/v1/comment/getList/item/(?P<pk>\d+)/$', views.getCommentList, name='getCommentList')
]