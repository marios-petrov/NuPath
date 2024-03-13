from django.utils.dateparse import parse_time
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse
from .forms import AddCalendarEvent
from .models import *
from datetime import date

# Create your views here.
@xframe_options_exempt #iframe capability
def doodlespace(request):
    return render(request, 'doodlespace.html')

@require_http_methods(["GET","POST"])
def dorms(request):

    # Querysets for the context
    dorms = Dorms.objects.all() #all the dorms available
    current_dorm = Dorms.objects.filter(is_current_dorm=True).first() #user's current dorm
    #using first() is supposed to be bad practice but there shouldn't be anything else in this list!
    checklist = UserChecklist.objects.all().first() #this should be user=request.user when users are linked, instead of first()

    #GPT generated
    if request.method == 'POST': 
        user_checklist = checklist #right now this is because it's grabbing the first one, but this might not be needed in the future
        for field in user_checklist._meta.fields: #for boolean field in the user checklist
            field_name = field.name #capture the field
            if field_name != 'user' and field_name in request.POST: #if the field isn't the user field and is the request
                field_value = request.POST.getlist(field_name) #when it's checked it returns a list like ['on', 'off']
                setattr(user_checklist, field_name, field_value[0] == 'on') #so you can just bool using the index where 'on' would appear! it immediately is off otherwise
        user_checklist.save()
        return redirect('dorms')
    
    context = {
        'dorms': dorms,
        'current_dorm': current_dorm,
        'checklist': checklist
    }
    return render(request, 'dorms.html', context) 

@require_http_methods(["GET", "POST"])
def dormview(request, dorm): 
    """Shows a dorm object from the dorms page. Allows user to select the dorm as their current dorm.
    Deselects any other dorm they have selected currently.

    Args:
        request: any http method request that comes from the dormview page.
        dorm (int): The object id of the dorm object. 

    Returns:
        render(request, dormview, context): _description_
    """
    dorm = Dorms.objects.get(id=dorm)
    current_dorm = Dorms.objects.filter(is_current_dorm=True)

    if request.method == "POST":
        if 'select' in request.POST: 
            current_dormview = request.POST.get('current_dormview', '') # gets object id to set it to true/false!
            dormselect = Dorms.objects.get(id=current_dormview) #get just the dorm you're looking at
            dormselect.is_current_dorm = not dormselect.is_current_dorm #toggle the dorm
            dormselect.save()

        for other_dorm in current_dorm: # unselects anything other dorm selected as true!
            if other_dorm != dormselect:
                other_dorm.is_current_dorm = False
                other_dorm.save() #don't forget to save!
    
        return redirect('dormview', dorm=dorm.id)

    context = {
        'dorm': dorm,
        'current_dorm': current_dorm
    }
    
    return render(request, 'dormview.html', context)

# Create your views here.
def doodlespace(request):
    return render(request, 'Features/doodlespace.html')

def home(request):
    return render(request, 'Features/home.html')

""" 
 quotes_obj = Quotes.objects.first()  # Assuming you only have one Quotes object

    # Get the quote bank from the Quotes object
    quote_bank = quotes_obj.get_quotebank()

    # Choose a random quote from the quote bank
    random_quote = random.choice(quote_bank)
"""

@require_http_methods(["GET"])
def catalyst(request):
    quotes = Quotes.objects.first() #this should be user=request.user when users are linked

    if date.weekday == 6: #should change quote every sunday
        #there could be quote rotation checks, but by that point i would just refactor the basis of this whole function
        shownquote = quotes.get_random_quote
        quotes.save()
    else:
        shownquote = quotes.last_displayed_quote

    
    return render(request, 'catalyst.html', {'shownquote' : shownquote})

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

def calendar(request):
    calendar_events = CalendarEvent.objects.all();
    if request.method == 'POST':
        event_form = AddCalendarEvent(request.POST or None)
        if event_form.is_valid():
            event_form.save()
            return render(request, 'Features/calendar.html', {'events': calendar_events})
    else:
        return render(request, 'Features/calendar.html', {'events': calendar_events})

