from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def todoList(request):
    return render(request, 'todolist.html')
