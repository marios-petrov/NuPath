from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
# cool that i replaced that with *?

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        badge_form = BadgesForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid() and badge_form.is_valid():
            u_form.save()
            p_form.save()
            badge_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        badge_form = BadgesForm(instance=request.user.profile)


    pf = request.user.profile
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'badge_form': badge_form,
        'picked_classes': pf.picked_classes, # added profile boolean fields to context to render the badges/checks
        'picked_dorm_room': pf.picked_dorm_room,
        'checked_ham_menu': pf.checked_ham_menu,
        'checked_campus_facilities': pf.checked_campus_facilities,
        'known_faculty': pf.known_faculty
    }

    return render(request, 'Users/profile.html', context)