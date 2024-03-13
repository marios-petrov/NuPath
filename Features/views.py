import base64
import json  # Import json for parsing the request body
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseForbidden
from .models import *
from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from .models import CalendarEvent
from .forms import AddCalendarEvent
from django.contrib.auth.decorators import login_required
import datetime
from Users.models import Profile # for leaderboard page
from django.db.models import Q # for 'or' statements in filters
from django.db.models import Count, F

@login_required
def home(request):
    # Fetch the top 5 most recent doodles
    recent_doodles = Doodle.objects.all().order_by('-created_at')[:4]

    # Calculate the highest upvote ratio
    highest_upvote_ratio_post = Post.objects.annotate(
        upvote_ratio=Count('upvotes') - Count('downvotes')
    ).order_by('-upvote_ratio').first()

    context = {
        'youtube_api_key': 'AIzaSyA7iyQqwPGI-5wXDmwgm84zdVQEno9OyiM',
        'channel_id': 'UCeGK7w0jvoIKUaGgGlit59Q',
        'recent_doodles': recent_doodles,
        'highest_upvote_ratio_post': highest_upvote_ratio_post,
    }
    return render(request, 'Features/home.html', context)

@login_required
def resources(request):
    return render(request, 'Features/resources.html')

@login_required
def catalyst(request):
    return render(request, 'Features/catalyst.html')

@login_required
def community(request):
    return render(request, 'Features/community.html')
@require_POST
@login_required
def save_doodle(request):
    # Parse the JSON body of the request
    data = json.loads(request.body)
    image_data = data.get('image_data')
    if image_data:
        # Split the base64 string
        format, imgstr = image_data.split(';base64,')
        # Extract the image file extension
        ext = format.split('/')[-1]

        # Convert base64 to image file
        image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        # Save the image to a new Doodle object
        Doodle.objects.create(user=request.user, image=image)

        return JsonResponse({'message': 'Doodle saved successfully!'})
    else:
        return JsonResponse({'error': 'No image data provided.'}, status=400)

@login_required
def doodlespace(request):
    return render(request, 'Features/doodlespace.html')


# view for deleting calendar event, GPT chat link that helped create it below:
# https://chat.openai.com/share/ef154ed4-f499-4712-890c-9113af4dfe38
@require_POST
@login_required
def delete_calendar_event(request):
    # Extract the event ID from the request data
    event_id = request.POST.get('event_id')

    # Retrieve the event object from the database
    event = get_object_or_404(CalendarEvent, pk=event_id)

    # Delete the event from the database
    if event.author is not None:  # can't delete academic calendar events silly!
        event.delete()

    # Return a success response
    return JsonResponse({'success': True})


@require_POST
@login_required
def add_calendar_event(request):
    # not ideal to have another view but it fixed the glaring dupe bug
    event_form = AddCalendarEvent(request.POST or None)
    if event_form.is_valid():
        new_event = event_form.save(commit=False)
        new_event.author = request.user
        new_event.save()
        # shouldn't need a many-to-many save afaik, event doesn't explicitly have that relationship with anything
        return redirect('/calendar/')


@login_required
def calendar(request):
    calendar_events = CalendarEvent.objects.all().filter(Q(author=request.user) | Q(author=None));
    # calendar events where author is None are academic calendar events
    today = datetime.datetime.now()
    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    end = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    todays_events = CalendarEvent.objects.filter(Q(author=request.user) | Q(author=None),
                                                 start_time__range=(start, end))
    # ^ the events filtered for the ones happening today
    return render(request, 'Features/calendar.html', {'events': calendar_events, 'todays_events': todays_events})


@login_required
def leaderboard(request):
    leaderboard_members = Profile.objects.all().filter(
        picked_classes=True,
        picked_dorm_room=True,
        checked_ham_menu=True,
        checked_campus_facilities=True,
        known_faculty=True
    )  # get all profiles with fully completed onboarding tasks

    return render(request, 'Features/leaderboard.html', {'members': leaderboard_members})

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'Features/community.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title and content:  # Simple validation
            Post.objects.create(title=title, content=content, author=request.user, date_posted=timezone.now())
            return redirect('community-home')
    # Redirect to the community page if not POST or if POST data is invalid
    return redirect('community-home')

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    if request.method == 'POST':
        post.delete()
        return redirect('community-home')
    else:
        # For safety, only allow POST requests to delete a post
        return HttpResponseForbidden()

@login_required
def upvote_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.downvotes.all():
            post.downvotes.remove(request.user)
        post.upvotes.add(request.user)
        return JsonResponse({'success': True, 'upvotes': post.upvotes.count(), 'downvotes': post.downvotes.count()})
    return JsonResponse({'success': False})

@login_required
def downvote_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.upvotes.all():
            post.upvotes.remove(request.user)
        post.downvotes.add(request.user)
        return JsonResponse({'success': True, 'upvotes': post.upvotes.count(), 'downvotes': post.downvotes.count()})
    return JsonResponse({'success': False})

