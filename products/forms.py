from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'publication_date', 'author', 'price', 'pages', 'book_type', )