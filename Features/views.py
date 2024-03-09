from django.utils.dateparse import parse_time
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from .models import CalendarEvent
from .forms import AddCalendarEvent

# Create your views here.
def doodlespace(request):
    return render(request, 'Features/doodlespace.html')

def home(request):
    return render(request, 'Features/home.html')

# view for deleting calendar event, GPT chat link that helped create it below:
# https://chat.openai.com/share/ef154ed4-f499-4712-890c-9113af4dfe38
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

@require_POST
def add_calendar_event(request):
    # not ideal to have another view but it fixed the glaring dupe bug
    event_form = AddCalendarEvent(request.POST or None)
    if event_form.is_valid():
        event_form.save()
        return redirect('/calendar/')

def calendar(request):
    calendar_events = CalendarEvent.objects.all();
    return render(request, 'Features/calendar.html', {'events': calendar_events})
