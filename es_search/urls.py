from django.conf.urls import url

from es_search.views import *

urlpatterns = [
    url(r'^$', first, name='first'),
    url(r'^second/$', second, name='second'),
    url(r'^third/$', third, name='third'),
    url(r'^fourth/$', fourth, name='fourth'),
    url(r'^search_first/$', search_view_first, name='search_view_first'),
    url(r'^csv_first/$', csv_first, name='csv_first'),
    url(r'^search_second/$', search_view_second, name='search_view_second'),
    url(r'^csv_second/$', csv_second, name='csv_second'),
    url(r'^search_third/$', search_view_third, name='search_view_third'),
    url(r'^csv_third/$', csv_third, name='csv_third'),
    url(r'^search_fourth/$', search_view_fourth, name='search_view_fourth'),
    url(r'^csv_fourth/$', csv_fourth, name='csv_fourth'),
]
