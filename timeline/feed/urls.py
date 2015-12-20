__author__ = 'lgavinho'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^notification/$', views.notification),
    url(r'^notification/(?P<pk>[0-9]+)/$', views.notification_detail),
]