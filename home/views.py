from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomePage(TemplateView):

	template_name = 'home.html'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip