from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Game
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import GameForm, CommentForm

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


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


def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
    else:
        form = GameForm(instance=game)
    return save_game_form(request, form, 'products/includes/partial_game_update.html')


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

def accept_sell(request, game_id, author_id):
    user_author = get_object_or_404(User, pk=author_id)
    current_user = get_object_or_404(User, pk=request.user.id)
    
    # TODO
    # if user != current = 404
    is_accept = False
    if request.user:
        is_accept = True

    if is_accept:
        game = Game.objects.get(pk=game_id)
        game.accept()
        game.save()

    context = {'is_accept': is_accept, 'game': game, 'author_id': author_id}
    return render(request, 'products/accept_sell.html', context)