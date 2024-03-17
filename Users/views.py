from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *


def register(request):
    """
    Handle user registration.

    - If the request method is POST, attempt to create a new user account using the data provided in the form.
    - Validate the form data. If valid, save the new user and redirect to the login page with a success message.
    - If the request method is not POST (i.e., GET), display a blank registration form.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse object with the registration form rendered in the 'Users/register.html' template.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')  # Redirect to the login page
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})


@login_required
def profile(request):
    """
    Handle user profile updates.

    Allows users to update their general user information, profile details, and badge statuses.
    - Processes three forms: a user form (u_form), a profile form (p_form), and a badges form (badge_form).
    - If the request method is POST, validate and save the forms if valid, then redirect to the profile page with a success message.
    - For GET requests, instantiate the forms with the current user's data.
    - The context includes flags for various tasks (e.g., picked classes, dorm room) to manage badges or other UI elements based on user actions.

    Args:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse object with the profile forms rendered in the 'Users/profile.html' template.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        badge_form = BadgesForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid() and badge_form.is_valid():
            u_form.save()
            p_form.save()
            badge_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')  # Redirect back to the profile page to display the updated info

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        badge_form = BadgesForm(instance=request.user.profile)

    # Context preparation for rendering the profile page, including task completion flags
    pf = request.user.profile
    all_tasks_completed = all([
        pf.picked_classes,
        pf.picked_dorm_room,
        pf.checked_ham_menu,
        pf.checked_campus_facilities,
        pf.known_faculty
    ])  # Determines if all profile-related tasks are completed

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'badge_form': badge_form,
        'picked_classes': pf.picked_classes,
        'picked_dorm_room': pf.picked_dorm_room,
        'checked_ham_menu': pf.checked_ham_menu,
        'checked_campus_facilities': pf.checked_campus_facilities,
        'known_faculty': pf.known_faculty,
        'all_tasks_completed': all_tasks_completed
    }

    return render(request, 'Users/profile.html', context)