# softwareengineering1/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'templates/base.html')