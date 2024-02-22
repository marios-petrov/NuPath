from django import forms
from .models import CalendarEvent, CalendarGroup

class AddEventForm(forms.Form):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'startDate', 'endDate', 'description']
