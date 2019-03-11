from django import forms
from .models import SimpleAuthConnection


class SimpleAuthConnectionForm(forms.ModelForm):
    class Meta:
        model = SimpleAuthConnection
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput
        }
