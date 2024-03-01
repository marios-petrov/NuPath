from django.urls import path
from . import views

urlpatterns = [
path('', views.doodlespace, name='doodlespace'),
]