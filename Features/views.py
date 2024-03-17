import datetime
from Users.models import Profile # for leaderboard page
from django.db.models import Q # for 'or' statements in filters
from django.db.models import Count, F
import base64
import json  # Import json for parsing the request body
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from .forms import AddCalendarEvent
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, redirect
from .models import Post


@login_required
def home(request):
    """
    Renders the homepage with a context containing:
    - The four most recent 'Doodle' objects.
    - The 'Post' object with the highest upvote ratio.
    - YouTube API key and channel ID for YouTube API calls (if applicable).

    Assumes models 'Doodle' and 'Post' are defined with 'created_at',
    'upvotes', and 'downvotes' fields or properties.
    """
    # Fetch the top 4 most recent doodles
    recent_doodles = Doodle.objects.all().order_by('-created_at')[:4]

    # Calculate the highest upvote ratio among posts
    highest_upvote_ratio_post = Post.objects.annotate(
        upvote_ratio=Count('upvotes') - Count('downvotes')
    ).order_by('-upvote_ratio').first()

    # Context for rendering the template
    context = {
        'youtube_api_key': 'YOUR_YOUTUBE_API_KEY',  # Replace with your actual API key
        'channel_id': 'YOUR_CHANNEL_ID',  # Replace with your actual channel ID
        'recent_doodles': recent_doodles,
        'highest_upvote_ratio_post': highest_upvote_ratio_post,
    }
    return render(request, 'Features/home.html', context)

@login_required
def resources(request):
    """
    Renders the 'resources' page. No additional context is passed to the template.
    """
    return render(request, 'Features/resources.html')

@login_required
def community(request):
    """
    Renders the 'community' page. No additional context is passed to the template.
    """
    return render(request, 'Features/community.html')

@require_POST
@login_required
def save_doodle(request):
    """
    Saves a doodle image sent via POST request in base64 encoding.
    Expects a JSON object in the request body with a key 'image_data' containing the image data.

    Returns a JSON response indicating success or failure.
    """
    # Parse the JSON body of the request
    data = json.loads(request.body)
    image_data = data.get('image_data')

    if image_data:
        # Split the base64 string to separate the encoding prefix from the image data
        format, imgstr = image_data.split(';base64,')
        # Extract the image file extension
        ext = format.split('/')[-1]

        # Convert base64 encoded data to an image file
        image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        # Save the image to a new Doodle object
        Doodle.objects.create(user=request.user, image=image)

        return JsonResponse({'message': 'Doodle saved successfully!'})
    else:
        return JsonResponse({'error': 'No image data provided.'}, status=400)

@login_required
def doodlespace(request):
    """
    Renders the 'doodlespace' page. This page is meant for users to view and interact with doodles.
    No additional context is passed to the template.
    """
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
    """
    Fetches and displays a list of all posts ordered by their posting date in descending order.
    Renders the community page with the list of posts.
    """
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'Features/community.html', {'posts': posts})

@login_required
def post_create(request):
    """
    Handles the creation of a new post.
    If the request method is POST, it attempts to create a new post with the title and content
    provided in the request. Simple validation checks if title and content are present.
    Upon successful creation, redirects to the community homepage.
    If not a POST request or if validation fails, redirects to the community homepage.
    """
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        if title and content:  # Simple validation
            Post.objects.create(title=title, content=content, author=request.user, date_posted=timezone.now())
            return redirect('community-home')
    return redirect('community-home')

@login_required
def post_delete(request, pk):
    """
    Deletes a post specified by its primary key (pk) if the request method is POST and
    if the request user is the author of the post.
    Returns a 403 Forbidden response if the request user is not the author or if the request method is not POST.
    Redirects to the community homepage upon successful deletion.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    if request.method == 'POST':
        post.delete()
        return redirect('community-home')
    else:
        return HttpResponseForbidden()

@login_required
def upvote_post(request, pk):
    """
    Handles upvoting a post specified by its primary key (pk).
    If the user has downvoted the post before, the downvote is removed before adding the upvote.
    Only allows POST requests for upvoting to prevent CSRF attacks.
    Returns a JSON response with the success status and updated upvote and downvote counts.
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.downvotes.all():
            post.downvotes.remove(request.user)
        post.upvotes.add(request.user)
        return JsonResponse({'success': True, 'upvotes': post.upvotes.count(), 'downvotes': post.downvotes.count()})
    return JsonResponse({'success': False})

@login_required
def downvote_post(request, pk):
    """
    Handles downvoting a post specified by its primary key (pk).
    If the user has upvoted the post before, the upvote is removed before adding the downvote.
    Only allows POST requests for downvoting to prevent CSRF attacks.
    Returns a JSON response with the success status and updated upvote and downvote counts.
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.upvotes.all():
            post.upvotes.remove(request.user)
        post.downvotes.add(request.user)
        return JsonResponse({'success': True, 'upvotes': post.upvotes.count(), 'downvotes': post.downvotes.count()})
    return JsonResponse({'success': False})

@require_http_methods(["GET","POST"])
def dorms(request):

    # Querysets for the context
    dorms = Dorms.objects.all() #all the dorms available
    """
    current_dorm = Dorms.objects.filter(is_current_dorm=True).first() #user's current dorm
    #using first() is supposed to be bad practice but there shouldn't be anything else in this list!
    """
    try:
        checklist = UserChecklist.objects.get(user=request.user)
    except UserChecklist.DoesNotExist:
        # Handle the scenario where the user doesn't have a pre-made checklist
        # For example, create a new checklist for the user
        # You can adjust this logic based on your requirements
        checklist = UserChecklist.objects.create(user=request.user)
        return redirect('dorms')

    #GPT generated
    if request.method == 'POST':
        user_checklist = checklist #right now this is because it's grabbing the first one, but this might not be needed in the future
        for field in user_checklist._meta.fields: #for boolean field in the user checklist
            field_name = field.name #capture the field
            if field_name != 'user' and field_name in request.POST: #if the field isn't the user field and is the request
                field_value = request.POST.getlist(field_name) #when it's checked it returns a list like ['on', 'off']
                setattr(user_checklist, field_name, field_value[0] == 'on') #so you can just bool using the index where 'on' would appear! it immediately is off otherwise
        user_checklist.save()
        return redirect('dorms')

    context = {
        'dorms': dorms,
        #'current_dorm': current_dorm,
        'checklist': checklist
    }
    return render(request, 'Features/dorms.html', context)

@require_http_methods(["GET", "POST"])
def dormview(request, dorm):
    """Shows a dorm object from the dorms page. Allows user to select the dorm as their current dorm.
    Deselects any other dorm they have selected currently.

    Args:
        request: any http method request that comes from the dormview page.
        dorm (int): The object id of the dorm object.

    Returns:
        render(request, dormview, context): _description_
    """
    dorm = Dorms.objects.get(id=dorm)
    """
    current_dorm = Dorms.objects.filter(is_current_dorm=True)

    if request.method == "POST":
        if 'select' in request.POST:
            current_dormview = request.POST.get('current_dormview', '') # gets object id to set it to true/false!
            dormselect = Dorms.objects.get(id=current_dormview) #get just the dorm you're looking at
            dormselect.is_current_dorm = not dormselect.is_current_dorm #toggle the dorm
            dormselect.save()

        for other_dorm in current_dorm: # unselects anything other dorm selected as true!
            if other_dorm != dormselect:
                other_dorm.is_current_dorm = False
                other_dorm.save() #don't forget to save!

        return redirect('dormview', dorm=dorm.id)

        There's just straight up no time to fix this.
    """

    context = {
        'dorm': dorm,
        #'current_dorm': current_dorm
    }

    return render(request, 'Features/dormview.html', context)

@login_required
@require_http_methods(["GET"])
def catalyst(request): #edited to change once a day
    try:
        quotes = Quotes.objects.get(user=request.user)
    except Quotes.DoesNotExist:
        defaultquotebank = {
            "quotebank": [
                {"quote": "If you want to achieve greatness stop asking for permission.", "author": "Anonymous"},
                {"quote": "Things work out best for those who make the best of how things work out.", "author": "John Wooden"},
                {"quote": "To live a creative life, we must lose our fear of being wrong.", "author": "Anonymous"},
                {"quote": "If you are not willing to risk the usual you will have to settle for the ordinary.", "author": "Jim Rohn"},
            ]
        }
        quotes = Quotes.objects.create(user=request.user, quotebank=defaultquotebank, last_displayed_quote="If you want to achieve greatness stop asking for permission. - Anonymous")
        return redirect('dorms')

    today = timezone.now().date()
    last_updated = quotes.updated_at.date() if quotes.updated_at else None

    if last_updated != today: #should change quote every day
        #there could be quote rotation checks, but by that point i would just refactor the basis of this whole function
        shownquote = quotes.get_random_quote()  # Call get_random_quote method
        quotes.save()
    else:
        shownquote = quotes.get_lastquote()
        quotes.save()

    return render(request, 'Features/catalyst.html', {'shownquote' : shownquote})
