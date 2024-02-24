from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def notes(request):
    return HttpResponse("This is the notes page")