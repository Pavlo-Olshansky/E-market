from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.game_list, name='game_list'),
    url(r'^create/$', views.game_create, name='game_create'),
    url(r'^(?P<pk>\d+)/update/$', views.game_update, name='game_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.game_delete, name='game_delete'),
    url(r'^(?P<pk>\d+)/details/$', views.game_details, name='game_details'),


]
