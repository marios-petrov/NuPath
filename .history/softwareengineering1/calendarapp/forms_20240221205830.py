from django import forms
from .models import CalendarEvent, CalendarGroup

class AddEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'startTate', 'endTate', 'description']

