from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Game, Photo
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import GameForm, CommentForm, LoginPasswordForm, PhotoForm, PayPalPaymentsForm

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site             
from accounts.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.conf import settings
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import naturaltime

import stripe
import json
import urllib


def save_game_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():

            game = form.save(commit=False)
            game.author = request.user
            game.save()

            # form.save()
            data['form_is_valid'] = True
            games = Game.objects.filter(is_accepted=False)
            data['html_game_list'] = render_to_string('products/includes/partial_game_list.html', {
                'games': games, 'user': request.user
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def game_list(request):
    games = Game.objects.filter(is_accepted=False)
    return render(request, 'products/game_list.html', {'games': games})


def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
    else:
        form = GameForm()
    return save_game_form(request, form, 'products/includes/partial_game_create.html')

@login_required(login_url='/accounts/login/')
def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
    else:
        form = GameForm(instance=game)
    return save_game_form(request, form, 'products/includes/partial_game_update.html')

@login_required(login_url='/accounts/login/')
def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)
    data = dict()
    if request.method == 'POST':
        game.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        games = Game.objects.filter(is_accepted=False)
        data['html_game_list'] = render_to_string('products/includes/partial_game_list.html', {
            'games': games, 'user': request.user
        })
    else:
        context = {'game': game}
        data['html_form'] = render_to_string('products/includes/partial_game_delete.html',
            context,
            request=request,
        )

    return JsonResponse(data)


def game_details(request, pk):
    model = Game
    template_name = 'products/game_details.html'
    current_user = request.user
    game = Game.objects.get(pk=pk)
    photos = Photo.objects.filter(game_id=game.id)
    if request.user.id == game.author_id:
        is_own = True
    else:
        is_own = False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, prefix="comment")
        photo_form = PhotoForm(request.POST, request.FILES)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            
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
                    comment.email = current_user.email
                    comment.user = current_user.username
                else:
                    comment.user=request.POST['text'] 
                    comment.email=request.POST['email']
                comment.game = game
                comment.save()
                
                messages.success(request, 'New comment added with success!')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')


            
            redirect_url = reverse('products:game_details', args=(game.id,))
            return HttpResponseRedirect(redirect_url)

        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.game = game
            photo.save()
            redirect_url = reverse('products:game_details', args=(game.id,))
            return HttpResponseRedirect(redirect_url)

    else:
        photo_form = PhotoForm(request.POST, request.FILES)
        comment_form = CommentForm(prefix="comment")

    context = {
        'game': game,
        'comment_form': comment_form,
        'photo_form': photo_form,
        'photos': photos,
        'is_own': is_own,
        'current_user': current_user,
        'GOOGLE_RECAPTCHA_SECRET_KEY':settings.GOOGLE_RECAPTCHA_SECRET_KEY
    }
    
    return render(request, 'products/game_details.html', context)


@login_required(login_url='/accounts/login/')
def accept_sell(request, game_id, author_id):
    user_author = get_object_or_404(User, pk=author_id)
    current_user = get_object_or_404(User, pk=request.user.id)
    game = Game.objects.get(pk=game_id)
    message = ''
    stripe_publish_key = settings.STRIPE_PUBLISHABLE_KEY
    ammount = game.price*100
    if request.method == 'POST':

        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Token is created using Stripe.js or Checkout!
        # Get the payment token submitted by the form:
        token = request.POST['stripeToken'] 

        customer = stripe.Customer.create(
          email=current_user.email,
          source=token,
        )

        source=stripe.Source.create(
          type='bitcoin',
          amount=ammount,
          currency='usd',
          owner={
            "email": current_user.email
          }
        )
        # Charge the user's card:
        charge = stripe.Charge.create(
          amount=ammount,
          currency="usd",
          description="Buy a game",
          customer=customer.id,
        )

        # Update a game list without this game
        game.accept()
        game.save()
        user_author.userprofile.money += ammount

        # Send message to seller(request a login and pass)
        current_site = get_current_site(request)
        subject = 'Your account wont to buy!'
        message = render_to_string('products/login_password/login_pass_request_EMAIL.html', {
            'user_author': user_author,
            'current_user': current_user,
            'game': game,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(current_user.pk)),
            'token': account_activation_token.make_token(current_user),
        })
        user_author.email_user(subject, message)

        redirect_url = reverse('products:payment_success', args=(game_id, author_id,))
        return HttpResponseRedirect(redirect_url)
    
    host = request.get_host()

    paypal_dict = {
    "business": 'pavlo.olshansky@gmail.com',
    "amount": str(game.price)+'.00',
    "item_name": game.title,
    "invoice": game.id,
    "notify_url": "https://{}{}".format(host, reverse('paypal-ipn')),
    "return_url": "http://{}{}".format(host, reverse('products:payment_success', args=(game_id, author_id,))),
    "cancel_return": "http://{}{}".format(host, reverse('products:game_details', args=(game.id,))),
    "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
    }

    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        

    context = {'paypal_form': paypal_form, 'game': game, 'user_author': user_author, 'game': game, 'ammount': ammount, 'stripe_publish_key': stripe_publish_key, 'message': message}
    return render(request, 'products/accept_sell.html', context)


# Seller send login/pass by loginpassForm
@login_required(login_url='/accounts/login/')
def send_login_password(request, uidb64, token, game_id, author_id, buyer_id):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    game = Game.objects.get(pk=game_id)
    user_author = User.objects.get(pk=author_id)
    current_site = get_current_site(request)

    # If token correct
    if current_user is not None and account_activation_token.check_token(current_user, token):
        
        # if login and pass inputed
        if request.method == 'POST':
            login_pass_request_form = LoginPasswordForm(request.POST)
            if login_pass_request_form.is_valid():
                login_pass = login_pass_request_form.save(commit=False)

                login_pass.game = game
                login_pass.owner = user_author 
                login_pass.save()

                subject = 'Login and pass to test account'
                message = render_to_string('products/login_password/login_pass_EMAIL.html', {
                    'user_author': user_author,
                    'current_user': current_user,
                    'game': game,
                    'domain': current_site.domain,
                    'login_pass': login_pass,
                })
                current_user.email_user(subject, message)

                redirect_url = reverse('products:login_pass_request_success', args=(game_id,))
                return HttpResponseRedirect(redirect_url)

        else:
            login_pass_request_form = LoginPasswordForm()

        user_author = User.objects.get(pk=author_id)
        current_user = User.objects.get(pk=buyer_id)

        context = {
            'user_author': user_author,
            'current_user': current_user,
            'game': game,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(current_user.pk)),
            'token': account_activation_token.make_token(current_user),
            'login_pass_request_form': login_pass_request_form,

        }
        
        return render(request, 'products/login_password/login_pass_form.html', context)

    else:
        
        return render(request, 'registration/account_activation_invalid.html')


@login_required(login_url='/accounts/login/')
def login_pass_request_success(request, game_id):
    game = Game.objects.get(pk=game_id)
    context = {'game': game}
    return render(request, 'products/login_password/login_pass_request_success.html', context)


@login_required(login_url='/accounts/login/')
def payment_success(request, game_id, author_id):
    game = Game.objects.get(pk=game_id)
    user_author = User.objects.get(pk=author_id)
    current_user = get_object_or_404(User, pk=request.user.id)

    context = {
            'user_author': user_author,
            'game': game,
            }
    return render(request, 'products/payment_successfull.html', context)


@login_required(login_url='/accounts/login/')
def money_out(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payout = stripe.Payout.create(
      amount=1,
      currency="usd",
    )

    return render(request, 'products/payout_successfull.html')