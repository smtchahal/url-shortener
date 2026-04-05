from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

from . import views

app_name = 'url_shortener'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<alias>[a-zA-Z0-9-_]+)$', views.redirect, name='alias'),
    url(r'^(?P<alias>[a-zA-Z0-9-_]+)(?P<extra>/.*)$', views.redirect, name='alias'),
    url(r'^(?P<alias>[a-zA-Z0-9-_]+)\+$', views.preview, name='preview'),
    url(r'^~analytics/$', views.analytics, name='analytics'),
    url(r'^~static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
