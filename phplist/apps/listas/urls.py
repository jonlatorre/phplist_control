from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from views import *
from models import *


urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            model=Lista,
            context_object_name='listas',
            template_name='listas_list.html')),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Lista,
            context_object_name='lista',
            template_name='listas_detail.html')),
    url(r'^sitios/$',
        ListView.as_view(
            model=Sitio,
            context_object_name='sitios',
            template_name='sitios_list.html')),
    url(r'^sitios/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Sitio,
            context_object_name='sitios',
            template_name='sitios_detail.html')),
)
