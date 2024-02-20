from django.shortcuts import render
import HTTPResponse from django.http

# Create your views here.
def todoList(request):
    return HTTPResponse("This is the todo list page")