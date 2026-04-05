from django.conf import settings
from django.urls import re_path
from django.views.static import serve

from . import views

app_name = 'url_shortener'
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)$', views.redirect, name='alias'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)(?P<extra>/.*)$', views.redirect, name='alias'),
    re_path(r'^(?P<alias>[a-zA-Z0-9-_]+)\+$', views.preview, name='preview'),
    re_path(r'^~analytics/$', views.analytics, name='analytics'),
    re_path(r'^~static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
