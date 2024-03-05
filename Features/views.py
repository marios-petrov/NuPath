from django.utils.dateparse import parse_time
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import *

# Create your views here.
def doodlespace(request):
    return render(request, 'doodlespace.html')

@require_http_methods(["GET", "POST"])
def dorms(request): #TODO - just return the user's dorm
    if request.method == "POST":
        action = request.POST.get('action')

    if action == '':
        # Capture the additional time and days fields
        course_name = request.POST.get('course_name', '')
        
    return redirect('dormview.html')

@require_http_methods(["GET", "POST"])
def dormview(request): #TODO - allow user to select dorm, GET should send jinja the dorm & lists associated
    if request.method == "POST":
        action = request.POST.get('action')

    return render(request, 'dormview.html')
