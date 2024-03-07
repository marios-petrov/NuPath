from django.utils.dateparse import parse_time
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import *

# Create your views here.
def doodlespace(request):
    return render(request, 'doodlespace.html')

#@require_http_methods(["GET", "POST"])
def dorms(request): #TODO - just return the user's dorm

    # Querysets for the context
    dorms = Dorms.objects.all() #this is here to display all the dorms available
    current_dorm = Dorms.objects.filter(is_current_dorm=True) #this is here to display the user's current dorm

    context = {
        'dorms': dorms,
        'current_dorm': current_dorm #TODO - make this only return a list or something
    }
    return render(request, 'dorms.html', context) 

@require_http_methods(["GET", "POST"])
def dormview(request, dorm): #TODO - allow user to select dorm, GET should send jinja the dorm & lists associated
    dorm = Dorms.objects.get(id=dorm)

    if request.method == "POST":
        if 'select' in request.POST:
            current_dormview = request.POST.get('current_dormview', '')
            dormselect = Dorms.objects.get(id=current_dormview)
            dormselect.is_current_dorm = not dormselect.is_current_dorm
            dormselect.save()
        return redirect('dormview', dorm=dorm.id)

    context = {
        'dorm': dorm,
    }
    
    return render(request, 'dormview.html', context)
