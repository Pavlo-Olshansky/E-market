from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Game

from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import GameForm


class ProductsPage(TemplateView):

	template_name = 'products/products_page.html'


def save_game_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            games = Game.objects.all()
            data['html_game_list'] = render_to_string('products/includes/partial_game_list.html', {
                'games': games
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def game_list(request):
    games = Game.objects.all()
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
            'games': games
        })
    else:
        context = {'game': game}
        data['html_form'] = render_to_string('products/includes/partial_game_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)