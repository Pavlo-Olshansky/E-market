from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

from PIL import Image
from django import forms
from django.core.files import File
# from .models import Photo
from django.forms.widgets import FileInput


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # def save(self, commit=True):
    # 	user = super(SignUpForm, self).save(commit=False)
    # 	user.email = cleaned_data['email']
    # 	user.first_name = cleaned_data['first_name']
    # 	user.last_name = cleaned_data['last_name']

    # 	user.save()

    # 	return user

class EditUserForm(UserChangeForm):

    template_name = '/accounts/change_password.html'
	
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        # exclude = ()


class EditProfileForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    file = forms.FileField(widget=FileInput)

    class Meta:
        model = UserProfile
        fields = ('file', 'x', 'y', 'width', 'height', )

    def save(self):
        photo = super(EditProfileForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')


        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo

