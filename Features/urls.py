from django.urls import path
from . import views

urlpatterns = [
path('', views.doodlespace, name='doodlespace'),
path('', views.dorms, name='dorms'),
path('/dormview', views.dorms, name='dormview') #check if ths is right later
]