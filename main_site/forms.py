import django.forms as forms
from django.forms import ModelForm
from .models import User



class UserForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password'}), required=True, min_length=6)
    spotify_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'spotify_name'}), required=True)
    class Meta:
        model = User
        fields = ["username", "password", "spotify_name"]
