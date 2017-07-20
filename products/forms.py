from django import forms
from .models import Game, Comment, LoginPassword
from PIL import Image
from django import forms
from django.core.files import File
from .models import Photo
from paypal.standard.forms import PayPalPaymentsForm


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


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )


class PayPalPaymentsForm(PayPalPaymentsForm):
    def get_image(self):
        return '/static/images/PayPal_button.png'
