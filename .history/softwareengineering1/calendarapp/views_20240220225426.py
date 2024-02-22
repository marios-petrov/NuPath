from django.shortcuts import render
from .models import CalendarEvent, CalendarGroup

# Create your views here.
def calendar(request):
    calendear_events = CalendarEvent.objects.all()
    calendar_groups = CalendarGroup.objects.all()
    return render(request, 'calendar.html', {})
