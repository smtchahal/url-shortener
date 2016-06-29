from django.conf.urls import url

from . import views

app_name = 'url_shortener'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<alias>[a-zA-Z0-9-_]+)$', views.redirect, name='short_url'),
    url(r'^(?P<alias>[a-zA-Z0-9-_]+)(?P<extra>/.*)$', views.redirect, name='short_url'),
    url(r'^(?P<alias>[a-zA-Z0-9-_]+)\+$', views.preview, name='preview'),
]
