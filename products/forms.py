from django import forms
from .models import Game, Comment

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'price', 'pages', 'game_type', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'email', 'body')