from django.urls import path
from . import views

urlpatterns = [
# Home Page
path('home/', views.home, name='home'),

# Community Page
path('home/', views.home, name='home'),

# Planning page
path('calendar/', views.calendar, name='calendar'),
path('delete_calendar_event/', views.delete_calendar_event, name='delete_calendar_event'),

#

# Doodle Page
path('doodlespace/', views.doodlespace, name='doodlespace'),



]