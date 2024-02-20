## help from chat gpt

from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.timer_page, name='timer_page')
]