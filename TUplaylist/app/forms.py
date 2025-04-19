from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


# Profile Forms
#=====================================================================================================
class RegistrationForm(forms.ModelForm):
    username = forms.CharField(validators=[no_spaces])
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput(), label="Repeat Password")
    agree_privacy = forms.BooleanField(label="I agree with the privacy policy")
    agree_show_profile = forms.BooleanField(label="I agree for my profile to be shown")
    agree_rules = forms.BooleanField(label="I agree to the site rules")
    class Meta:
        model = ProfileModel
        fields = [
            'username', 'password', 'repeat_password', 'username', 'email', 'agree_privacy', 'agree_show_profile', 'agree_rules'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password and repeat_password and password != repeat_password:
            raise ValidationError("Passwords do not match. Please try again.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance



# Login Forms
#=====================================================================================================
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'



# Profile Edit Forms
#=====================================================================================================
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'bio']







class SongForm(forms.ModelForm):
    class Meta:
        model = SongModel
        fields = ['title', 'artist', 'artist_type', 'release_year', 'genre', 'cover', 'duration']

    def save(self, user=None, commit=True):
        song = super().save(commit=False)
        if user is not None:
            song.uploader = user
        if commit:
            song.save()
        return song


