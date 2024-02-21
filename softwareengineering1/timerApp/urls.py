## help from chat gpt

from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.timer_page, name='timer_page'),
    path('start_timer/<int:timer_id>/', views.start_timer, name='start_timer'),
    path('stop_timer/<int:timer_id>/', views.stop_timer, name='stop_timer')
]