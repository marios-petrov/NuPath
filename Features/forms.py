from django import forms
from .models import CalendarEvent

class AddCalendarEvent(forms.ModelForm):
	class Meta:
		model = CalendarEvent
		fields = ['title', 'description', 'start_time']