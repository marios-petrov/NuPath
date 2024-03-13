from django.urls import path
from . import views

urlpatterns = [
    path('delete_calendar_event/', views.delete_calendar_event, name='delete_calendar_event'),
    path('doodlespace/', views.doodlespace, name='doodlespace'),
    path('home/', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    path('dorms', views.dorms, name='dorms'),
    path('dormview/<int:dorm>', views.dormview, name='dormview'), 
    path('catalyst/', views.catalyst, name='catalyst')
]