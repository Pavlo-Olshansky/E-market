from django.conf.urls import url
from . import views
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = [

    # Our team url
    url(r'^our_team/$', TemplateView.as_view(
    	template_name='get_in_touch/our_team.html'), name='our_team'),
    ## Pavlo Olshansky
    url(r'^our_team/Pavlo_Olshansky', TemplateView.as_view(
    	template_name='get_in_touch/BIO/Pavlo_Olshansky.html'), name='Pavlo_Olshansky'),
    ## Volodymyr Tysovskyi
    url(r'^our_team/Volodymyr_Tysovskyi', TemplateView.as_view(
    	template_name='get_in_touch/BIO/Volodymyr_Tysovskyi.html'), name='Volodymyr_Tysovskyi'),
    ## Yuri Bakalov
    url(r'^our_team/Yuri_Bakalov', TemplateView.as_view(
    	template_name='get_in_touch/BIO/Yuri_Bakalov.html'), name='Yuri_Bakalov'),
    ## Ivan Sytar
    url(r'^our_team/Ivan_Sytar', TemplateView.as_view(
    	template_name='get_in_touch/BIO/Ivan_Sytar.html'), name='Ivan_Sytar'),

    # Contact Us
    url(r'^contact_us/$', views.contact_us, name='contact_us'),

    # Support center
    url(r'^support/$', views.support, name='support'),
]
