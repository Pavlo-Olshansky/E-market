from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$', views.signup, name='signup'),

    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]
