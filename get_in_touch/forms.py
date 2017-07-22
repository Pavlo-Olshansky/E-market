from django import forms
from .models import Contact_us, Support


class Contact_us_form(forms.ModelForm):
    class Meta:
        model = Contact_us
        fields = ('body',)

class SupportForm(forms.ModelForm):
	class Meta:
		model = Support
		fields = ('problem', 'body')