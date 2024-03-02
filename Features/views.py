from django.utils.dateparse import parse_time
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import *

# Create your views here.
def doodlespace(request):
    return render(request, 'Features/doodlespace.html')

def home(request):
    return render(request, 'Features/home.html')
