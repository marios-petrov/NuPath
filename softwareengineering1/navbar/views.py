from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def navbar(request):
  template = loader.get_template('navbar.html')
  return HttpResponse(template.render())