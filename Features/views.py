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
from datetime import date



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
        'youtube_api_key': '',
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

@require_POST
@login_required
def add_calendar_event(request):
    # not ideal to have another view but it fixed the glaring dupe bug
    event_form = AddCalendarEvent(request.POST or None)
    if event_form.is_valid():
        event_form.save()
        return redirect('/calendar/')

@require_POST
@login_required
def delete_calendar_event(request):
    # Extract the event ID from the request data
    event_id = request.POST.get('event_id')

    # Retrieve the event object from the database
    event = get_object_or_404(CalendarEvent, pk=event_id)

    # Delete the event from the database
    event.delete()

    # Return a success response
    return JsonResponse({'success': True})

@login_required
def calendar(request):
    calendar_events = CalendarEvent.objects.all();
    if request.method == 'POST':
        event_form = AddCalendarEvent(request.POST or None)
        if event_form.is_valid():
            event_form.save()
            return render(request, 'Features/calendar.html', {'events': calendar_events})
    else:
        return render(request, 'Features/calendar.html', {'events': calendar_events})

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


@require_http_methods(["GET","POST"])
def dorms(request):

    dorms = Dorms.objects.all() #all the dorms available
    current_dorm = Dorms.objects.filter(is_current_dorm=True).first() #user's current dorm
    #using first() is supposed to be bad practice but there shouldn't be anything else in this list!
    checklist = UserChecklist.objects.all().first() #this should be user=request.user when users are linked, instead of first()

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
        'current_dorm': current_dorm,
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

    context = {
        'dorm': dorm,
        'current_dorm': current_dorm
    }
    
    return render(request, 'Features/dormview.html', context)

# Create your views here.
def doodlespace(request):
    return render(request, 'Features/doodlespace.html')

def home(request):
    return render(request, 'Features/home.html')

@require_http_methods(["GET"])
def catalyst(request):
    quotes = Quotes.objects.first() #this should be user=request.user when users are linked

    if date.weekday == 6: #should change quote every sunday
        #there could be quote rotation checks, but by that point i would just refactor the basis of this whole function
        shownquote = quotes.get_random_quote
        quotes.save()
    else:
        shownquote = quotes.last_displayed_quote

    
    return render(request, 'Features/catalyst.html', {'shownquote' : shownquote})

