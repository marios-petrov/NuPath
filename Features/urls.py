from django.urls import path
from . import views

urlpatterns = [
path('', views.doodlespace, name='doodlespace'),
path('dorms', views.dorms, name='dorms'),
path('dormview', views.dormview, name='dormview') 
]