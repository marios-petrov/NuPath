## help from chat gpt

from django.shortcuts import render, redirect
from .models import TimeSpent

def timer_page(request):
    timers = TimeSpent.objects.all()
    return render(request, 'timer.html', {'timers': timers})

def start_timer(request, timer_id):
    timer = TimeSpent.objects.get(id=timer_id)
    timer.startTimer()
    return redirect('timer_page')

def stop_timer(request, timer_id):
    timer = TimeSpent.objects.get(id=timer_id)
    timer.endTimer()
    return redirect('timer_page')
