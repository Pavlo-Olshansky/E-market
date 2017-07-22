from django.conf.urls import url
from . import views
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = [

    # Our team url
    url(r'^our_team/$', TemplateView.as_view(template_name='footer/our_team.html'), name='our_team'),

    # Contact Us
    url(r'^contact_us/$', views.contact_us, name='contact_us'),

    # Support center
    url(r'^support/$', views.support, name='support'),
]
