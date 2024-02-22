from django import forms

class AddEventForm(forms.Form):
    title = forms.CharField(max_length=64)
    startDate = forms.DateTimeField()
    endDate = forms.DateTimeField()
    description = forms.CharField(max_length=64)