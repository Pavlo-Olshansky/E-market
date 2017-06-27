from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [

	# Register new user
    url(r'^$', views.signup, name='signup'),

    # send an activation URL 
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),

    # activation URL
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]
