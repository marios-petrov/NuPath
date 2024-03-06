from django.utils.dateparse import parse_time
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import CalendarEvent
from .forms import AddCalendarEvent

# Create your views here.
def doodlespace(request):
    return render(request, 'Features/doodlespace.html')

def home(request):
    return render(request, 'Features/home.html')

def calendar(request):
    calendar_events = CalendarEvent.objects.all();
    if request.method == 'POST':
        event_form = AddCalendarEvent(request.POST or None)
        if event_form.is_valid():
            event_form.save()
            return render(request, 'Features/calendar.html', {'events': calendar_events})
    else:
        return render(request, 'Features/calendar.html', {'events': calendar_events})
