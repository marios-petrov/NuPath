from django.shortcuts import render
import HttpResponse from django.http

# Create your views here.
def notifications(request):
    return HttpResponse("This is the todo list page")