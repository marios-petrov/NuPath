from django.shortcuts import render
from .models import CalendarEvent, CalendarGroup
from .forms import AddEventForm

# Create your views here.
def calendar(request):
    calendear_events = CalendarEvent.objects.all()
    calendar_groups = CalendarGroup.objects.all()
    return render(request, 'calendar.html', {'events': calendear_events, 'groups': calendar_groups})

def dataTest(request):
    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        if eventForm.is_valid():
            return render(request, 'dataTest.html', {'events': calendear_events, 'groups': calendar_groups})
    calendear_events = CalendarEvent.objects.all()
    calendar_groups = CalendarGroup.objects.all()
    return render(request, 'dataTest.html', {'events': calendear_events, 'groups': calendar_groups})