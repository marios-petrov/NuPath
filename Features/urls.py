from django.urls import path
from . import views

urlpatterns = [
path('doodlespace/', views.doodlespace, name='doodlespace'),
path('home/', views.home, name='home'),
]