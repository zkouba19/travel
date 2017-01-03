from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^homepage/$', views.homepage),
    url(r'^join/(?P<id>\d*)/$', views.join),
    url(r'^viewtrip/(?P<id>\d*)/$', views.viewtrip),
    url(r'^newtrip/$', views.newtrip),
    url(r'^newtrip/add/$', views.add_trip),
]