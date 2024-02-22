from django.shortcuts import render
from .models import CalendarEvent, CalendarGroup
from .forms import AddEventForm

# Create your views here.
def calendar(request):
    calendear_events = CalendarEvent.objects.all()
    calendar_groups = CalendarGroup.objects.all()
    if request.method == 'POST':
        eventForm = AddEventForm(request.POST or None)
        if eventForm.is_valid():
            eventForm.save()
            return render(request, 'calendar.html', {'events': calendear_events, 'groups': calendar_groups})
    else:
        return render(request, 'dataTest.html', {'events': calendear_events, 'groups': calendar_groups})
