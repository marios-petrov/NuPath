from django import forms
from .models import CalendarEvent, CalendarGroup

class AddEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'startDate', 'endDate', 'description']

