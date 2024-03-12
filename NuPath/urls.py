"""
URL configuration for NuPath project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Features import views as features_views
from Users import views as user_views

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('admin/', admin.site.urls),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('', features_views.home, name='root_home'),
    path('home/', features_views.home, name='home'),

    path('resources/', features_views.resources, name='resources'),
    path('community/', features_views.community, name='community'),
    #path('catalyst/', features_views.catalyst, name='catalyst'),

    path('calendar/', features_views.calendar, name='calendar'),
    path('add_calendar_event/', features_views.add_calendar_event, name='add_calendar_event'),
    path('delete_calendar_event/', features_views.delete_calendar_event, name='delete_calendar_event'),

    path('doodlespace/', features_views.doodlespace, name='doodlespace'),
    path('save_doodle/', features_views.save_doodle, name='save_doodle'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
