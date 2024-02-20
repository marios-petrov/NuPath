from django.shortcuts import render

# Create your views here.
def todoList(request):
    return HTTPResponse("This is the todo list page")