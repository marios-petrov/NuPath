from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class BadgesForm(forms.ModelForm):
    task1 = forms.BooleanField(label='Picked classes and added them to your calendar', required=False)
    task2 = forms.BooleanField(label='Picked a dorm room', required=False)
    task3 = forms.BooleanField(label='Checked out the HAM menu', required=False)
    task4 = forms.BooleanField(label='Checked out campus facilities', required=False)
    task5 = forms.BooleanField(label='Gotten to know our faculty', required=False)

    class Meta:
        model = Profile
        # fields = []