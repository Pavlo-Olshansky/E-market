from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from .forms import Contact_us_form, SupportForm

import urllib
import json


def contact_us(request):

	if request.method == 'POST':
		form = Contact_us_form(request.POST)
		if form.is_valid():

			contact_us = form.save(commit=False)
			''' Begin reCAPTCHA validation '''
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {
				'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
				'response': recaptcha_response
			}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			''' End reCAPTCHA validation '''

			if result['success']:
				if request.user.is_authenticated:
					contact_us.email = request.user.email
					contact_us.user = request.user.username
					logined = True
				else:
					contact_us.user=request.POST['text'] 
					contact_us.email=request.POST['email']
					logined = False
				send_mail(
					'Contact Us from "{}" (Logined: {})'.format(contact_us.email, logined),
				    contact_us.body,
				    contact_us.email,
				    [settings.GMAIL_MAIL],
				    fail_silently=False,
				)
				contact_us.save()
                
			return render(request, 'footer/contact_us_success.html')


	else:
		form = Contact_us_form()

	context ={'form': form}
	return render(request, 'footer/contact_us.html', context)


def support(request):
	if request.method == 'POST':
		form = SupportForm(request.POST)
		if form.is_valid():

			support = form.save(commit=False)
			''' Begin reCAPTCHA validation '''
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {
				'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
				'response': recaptcha_response
			}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			''' End reCAPTCHA validation '''

			if result['success']:
				if request.user.is_authenticated:
					support.email = request.user.email
					support.user = request.user.username
					logined = True
				else:
					support.user=request.POST['text'] 
					support.email=request.POST['email']
					logined = False

				send_mail(
					'Support ({}) from "{}" (Logined: {})'.format(support.get_problem_display(), support.email, logined),
				    support.body,
				    support.email,
				    [settings.GMAIL_MAIL],
				    fail_silently=False,
				)
				support.save()
	            
			return render(request, 'footer/support_success.html')


	else:
		form = SupportForm()

	context ={'form': form}
	return render(request, 'footer/support.html', context)