from django import forms
from .models import Game, Comment, LoginPassword

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'price', 'game_type', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class LoginPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = LoginPassword
        fields = ('login', 'password')
