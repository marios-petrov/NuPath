from django.urls import path
from . import views

urlpatterns = [
    path('', views.todoList, name='todo list'),
]