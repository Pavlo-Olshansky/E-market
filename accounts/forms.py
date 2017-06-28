from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


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

class EditProfileForm(UserChangeForm):

    template_name = '/accounts/change_password.html'
	
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        # exclude = ()
