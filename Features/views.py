from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from .forms import AddCalendarEvent
from .models import *
import base64
import json  # Import json for parsing the request body
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Doodle
@login_required
def home(request):
    return render(request, 'Features/home.html')
@login_required
def resources(request):
    return render(request, 'Features/resources.html')
@require_POST
@login_required
def save_doodle(request):
    # Parse the JSON body of the request
    data = json.loads(request.body)
    image_data = data.get('image_data')
    if image_data:
        # Split the base64 string
        format, imgstr = image_data.split(';base64,')
        # Extract the image file extension
        ext = format.split('/')[-1]

        # Convert base64 to image file
        image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        # Save the image to a new Doodle object
        Doodle.objects.create(user=request.user, image=image)

        return JsonResponse({'message': 'Doodle saved successfully!'})
    else:
        return JsonResponse({'error': 'No image data provided.'}, status=400)

def doodlespace(request):
    return render(request, 'Features/doodlespace.html')

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
@login_required
def calendar(request):
    calendar_events = CalendarEvent.objects.all();
    if request.method == 'POST':
        event_form = AddCalendarEvent(request.POST or None)
        if event_form.is_valid():
            event_form.save()
            return render(request, 'Features/calendar.html', {'events': calendar_events})
    else:
        return render(request, 'Features/calendar.html', {'events': calendar_events})

