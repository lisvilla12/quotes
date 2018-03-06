from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main/$', views.main),
    url(r'login$', views.login),
    url(r'register$', views.register),
    url(r'quotes$', views.quotes),
    url(r'create$', views.create),
    url(r'addfav/(?P<id>\d+)$', views.addfav),
    url(r'removefav/(?P<id>\d+)$', views.removefav),
    url(r'users/(?P<id>\d+)$', views.users),
    url(r'logout$', views.logout)
]