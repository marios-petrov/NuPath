from django.utils.dateparse import parse_time
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from .models import CalendarEvent
from .forms import AddCalendarEvent
from django.contrib.auth.decorators import login_required
import datetime
from Users.models import Profile # for leaderboard page

# Create your views here.
@login_required
def doodlespace(request):
    return render(request, 'Features/doodlespace.html')

@login_required
def home(request):
    return render(request, 'Features/home.html')

# view for deleting calendar event, GPT chat link that helped create it below:
# https://chat.openai.com/share/ef154ed4-f499-4712-890c-9113af4dfe38
@require_POST
@login_required
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
@login_required
def add_calendar_event(request):
    # not ideal to have another view but it fixed the glaring dupe bug
    event_form = AddCalendarEvent(request.POST or None)
    if event_form.is_valid():
        new_event = event_form.save(commit=False)
        new_event.author = request.user
        new_event.save()
        # shouldn't need a many-to-many save afaik, event doesn't explicitly have that relationship with anything
        return redirect('/calendar/')

@login_required
def calendar(request):
    calendar_events = CalendarEvent.objects.all().filter(author = request.user);
    today = datetime.datetime.now()
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    todays_events = CalendarEvent.objects.filter(author=request.user, start_time__range=(start, end))
    # ^ the events filtered for the ones happening today
    return render(request, 'Features/calendar.html', {'events': calendar_events, 'todays_events': todays_events})

@login_required
def leaderboard(request):
    leaderboard_members = Profile.objects.all().filter(
        picked_classes = True,
        picked_dorm_room = True,
        checked_ham_menu = True,
        checked_campus_facilities = True,
        known_faculty = True
    ) # get all profiles with fully completed onboarding tasks

    return render(request, 'Features/leaderboard.html', {'members': leaderboard_members})