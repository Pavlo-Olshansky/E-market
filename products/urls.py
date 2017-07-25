from django.conf.urls import url, include
from . import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [

    url(r'^$', views.game_list, name='game_list'),
    url(r'^create/$', views.game_create, name='game_create'),
    url(r'^(?P<pk>\d+)/update/$', views.game_update, name='game_update'),
    url(r'^(?P<pk>\d+)/delete/$', views.game_delete, name='game_delete'),
    url(r'^(?P<pk>\d+)/details/$', views.game_details, name='game_details'),
    url(r'^(?P<game_id>\d+)/(?P<author_id>\d+)/accept', views.accept_sell, name='accept_sell'),

    url(r'^filter_game/$', views.filter_game, name='filter_game'),



    url(r'^send_login_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<game_id>\d+)/(?P<author_id>\d+)/(?P<buyer_id>\d+)', 
    	views.send_login_password, name='send_login_password'),

    url(r'^send_login_password/(?P<game_id>\d+)/success/$', views.login_pass_request_success, name='login_pass_request_success'),

    url(r'^payment/(?P<uuid>[\w-]+)/success/$', views.payment_success, name='payment_success'),

    url(r'^money/out/$', views.money_out, name='money_out'),

]