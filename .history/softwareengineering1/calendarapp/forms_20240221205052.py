from django import forms
from .models import CalendarEvent, CalendarGroup

class AddEventForm(forms.Form):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'startDate', 'endDate', 'description']

    def save(self):
        if self.is_valid():
            event = CalendarEvent(
                title=self.cleaned_data['title'],
                startDate=self.cleaned_data['startDate'],
                endDate=self.cleaned_data['endDate'],
                description=self.cleaned_data['description']
            )
            event.save()
            return event
        else:
            return None
