from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """
    A form for creating new users. Inherits from Django's UserCreationForm and adds an email field.

    Attributes:
        email (EmailField): An additional field for user email. Required for user registration.

    Meta:
        model (User): The Django default User model used for creating the form fields.
        fields (list): Specifies the fields to be used in the form. Includes username, email, password1 (password),
                       and password2 (password confirmation).
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """
    A form for updating user information. Specifically designed for updating username and email.

    Attributes:
        email (EmailField): Field for updating the user's email. Required for the form.

    Meta:
        model (User): The Django User model to which the form is tied.
        fields (list): Fields included in the form, allowing the user to update their username and email.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """
    A form for updating the user's profile, specifically the profile image.

    Meta:
        model (Profile): The custom Profile model related to the User model.
        fields (list): Defines the 'image' field for the form, allowing users to update their profile image.
    """

    class Meta:
        model = Profile
        fields = ['image']

class BadgesForm(forms.ModelForm):
    """
    A form for updating the status of various badges in the user's profile.

    Includes boolean fields for different achievements or tasks a user can complete.
    Fields are not required, allowing for partial updates.

    Meta:
        model (Profile): Specifies the Profile model to which this form is connected.
        fields (list): Includes boolean fields representing different badges or achievements
                       (e.g., 'picked_classes', 'picked_dorm_room', etc.).
    """
    # Here, required=False allows these fields to be optional in the form submission, supporting partial updates
    picked_classes = forms.BooleanField(required=False)
    picked_dorm_room = forms.BooleanField(required=False)
    checked_ham_menu = forms.BooleanField(required=False)
    checked_campus_facilities = forms.BooleanField(required=False)
    known_faculty = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ['picked_classes', 'picked_dorm_room', 'checked_ham_menu', 'checked_campus_facilities',
                  'known_faculty']
