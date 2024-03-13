from django import forms
from .models import *

class AddCalendarEvent(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'description', 'start_time']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']