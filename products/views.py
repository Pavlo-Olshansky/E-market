from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Game
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import GameForm, CommentForm, LoginPasswordForm

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site             
from accounts.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

@login_required(login_url='/accounts/login/')
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
        games = Game.objects.all()
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

    game = Game.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, prefix="comment")
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.game = game
            comment.save()
            redirect_url = reverse('products:game_details', args=(game.id,))
            return HttpResponseRedirect(redirect_url)

    else:
        comment_form = CommentForm(prefix="comment")
    
    is_own = False
    if request.user.id == game.author_id:
        is_own = True

    context = {
        'game': game,
        'comment_form': comment_form,
        'is_own': is_own,
    }
    
    return render(request, 'products/game_details.html', context)


@login_required(login_url='/accounts/login/')
def accept_sell(request, game_id, author_id):
    user_author = get_object_or_404(User, pk=author_id)
    current_user = get_object_or_404(User, pk=request.user.id)
    

    game = Game.objects.get(pk=game_id)

    # Send message to seller(request a login and pass)
    current_site = get_current_site(request)
    subject = 'Your account wont to buy!'
    message = render_to_string('products/email_messages/login_pass_request.html', {
        'user_author': user_author,
        'current_user': current_user,
        'game': game,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(current_user.pk)),
        'token': account_activation_token.make_token(current_user),
    })
    user_author.email_user(subject, message)

    context = {'game': game, 'user_author': user_author, 'game': game, 'message': message}

    return render(request, 'products/accept_sell.html', context)


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

                # Update a game list without this game
                game.accept()
                game.save()

                subject = 'Login and pass to test account'
                message = render_to_string('products/email_messages/login_pass_to_test.html', {
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
        
        return render(request, 'products/email_messages/login_pass_form.html', context)

    else:
        
        return render(request, 'registration/account_activation_invalid.html')


@login_required(login_url='/accounts/login/')
def login_pass_request_success(request, game_id):
    game = Game.objects.get(pk=game_id)
    context = {'game': game}
    return render(request, 'products/email_messages/login_pass_request_success.html', context)
