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
    picked_classes = forms.BooleanField(required=False)
    picked_dorm_room = forms.BooleanField(required=False)
    checked_ham_menu = forms.BooleanField(required=False)
    checked_campus_facilities = forms.BooleanField(required=False)
    known_faculty = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        # boolean fields
        fields = ['picked_classes', 'picked_dorm_room', 'checked_ham_menu', 'checked_campus_facilities',
                  'known_faculty']
        # I feel like this long list isn't ideal but wtv
