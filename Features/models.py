from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
import random


# model for a calendar event
class CalendarEvent(models.Model):

    """
    Represents a calendar event.
    Attributes:
        title (str): The title of the event.
        startTime (datetime): The start time of the event.
        description (str): The description of the event (optional).
        author (User): The user associated with the calendar event
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    start_time = models.DateTimeField() # dang is this all the event needs? feels too simple
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) # i think cascade should be okay
    # author is nullable, events with no author are hardcoded academic calendar events
    # CASCADE = delete other things with a reference to this
	# end-time, whether it repeats, etc to be added later (stretch goal)

    def __str__(self):
        if self.author is None:
            return f'Event{self.id} {self.title} @ {self.start_time} (hardcoded)'
        else:
            return f'Event{self.id} {self.title} @ {self.start_time} by user {self.author.username}'

# model for a doodle
class Doodle(models.Model):
    image = models.ImageField(upload_to='doodles/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doodle {self.id} by {self.user.username}"

# model for community post
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_posts', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class UserChecklist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    housing_registration = models.BooleanField(default=False)
    get_keys_from_housing = models.BooleanField(default=False)
    bedding = models.BooleanField(default=False)
    lamps = models.BooleanField(default=False)
    wastebasket_and_trash_bag = models.BooleanField(default=False)
    key_chain = models.BooleanField(default=False)
    clothes_hangers = models.BooleanField(default=False)
    clothing = models.BooleanField(default=False)
    bath_towel = models.BooleanField(default=False)
    bathrobe = models.BooleanField(default=False)
    toiletries = models.BooleanField(default=False)
    cleaning_supplies = models.BooleanField(default=False)
    room_deodorizing_spray = models.BooleanField(default=False)
    laundry_supplies = models.BooleanField(default=False)
    school_supplies = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Checklist'

class Dorms(models.Model):
    dormtype = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    #residents = models.ManyToManyField(User, null=True)

    #there's a better way to have several images, but i'd prefer to have a fixed three for each dorm.
    dormpic1 = models.ImageField(upload_to='dormview', default='default.webp', blank=True) #THIS ONLY WORKS WITH MEDIA FILE. FOR SOME REASON
    dormpic2 = models.ImageField(upload_to='dormview', default='default.webp', blank=True)
    dormpic3 = models.ImageField(upload_to='dormview', default='default.webp', blank=True)
    foodoptions = models.CharField(max_length=200, blank=True)

    is_current_dorm = models.BooleanField(default=False)
    #this is just to make the loaddata not mad atp
    """
    WE'RE NOT EVEN DOING THIS BECAUSE THERE'S NO TIME WHO CARES
    Talking to myself here so I don't forget, but we should store with the user what dorm they have
    saved & their dorm number to a profile. We would use a manytoone for this.
    It should be that a User can only pick one dorm, but that one dorm can be selected by many users.

    This field would be this, in a user profile:
        user_dorm = models.ForeignKey(Dorm, blank=True)
    Then, the views page for dormview would check whether the viewing user's dorm matched the page's dorm, rather than a boolean.
    """

    def __str__(self):
        return self.dormtype #returns name/type of dorm

    def get_address(self):
        return self.address #returns address as a string

    def get_foodoptions(self):
        return self.foodoptions #returns food options as a string

    def get_foodoptions_list(self):
        return str(self.foodoptions).split(', ') #returns food options as a list
    #the str() function is so i don't have to use an entire json processing function


class Quotes(models.Model):
    # I'm going to be honest I don't want to use a model for this but IDK where I'd store this...
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #This may be superfluous, but the idea is that everybody got a different quote, I think...

    quotebank = models.JSONField()
    last_displayed_quote = models.TextField(blank=True, null=True)  # Field to store the last displayed quote
    updated_at = models.DateTimeField(default=timezone.now)

    def get_random_quote(self): #gpt...
        if not self.quotebank:
            return None  # Return None if quote bank is empty

        # Extract the list of quotes from the quote bank
        quotes_list = self.quotebank.get("quotebank", [])

        # Use random.choice() to select a random quote from the list of quotes
        random_quote = random.choice(quotes_list)

        # Extract the quote text and author from the randomly selected quote
        quote = random_quote.get("quote", "")
        author = random_quote.get("author", "")
        self.last_displayed_quote = f"{quote} - {author}"  # Update last displayed quote
        self.save()  # Save changes to the model instance
        string = quote + ' - ' + author


        # Return the quote and author as two strings in a list
        return string #i hope this isnt too much logic in the models LOL

    def get_quotebank(self):
        return self.quotebank

    def get_lastquote(self):
        if self.last_displayed_quote == '':
            return self.get_random_quote
        return self.last_displayed_quote

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
