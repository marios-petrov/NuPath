from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


# Create your views here.
def timer(request):
    return HttpResponse("This is the timer page")