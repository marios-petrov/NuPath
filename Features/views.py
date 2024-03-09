from django.http import JsonResponse
from django.utils.dateparse import parse_time
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST

from .forms import AddCalendarEvent
from .models import *

# Create your views here.
def doodlespace(request):
    return render(request, 'Features/doodlespace.html')

def home(request):
    return render(request, 'Features/home.html')

def resources(request):
    return render(request, 'Features/resources.html')
@require_POST
def delete_calendar_event(request):
    # Extract the event ID from the request data
    event_id = request.POST.get('event_id')

    # Retrieve the event object from the database
    event = get_object_or_404(CalendarEvent, pk=event_id)

    # Delete the event from the database
    event.delete()

    # Return a success response
    return JsonResponse({'success': True})

def calendar(request):
    calendar_events = CalendarEvent.objects.all();
    if request.method == 'POST':
        event_form = AddCalendarEvent(request.POST or None)
        if event_form.is_valid():
            event_form.save()
            return render(request, 'Features/calendar.html', {'events': calendar_events})
    else:
        return render(request, 'Features/calendar.html', {'events': calendar_events})