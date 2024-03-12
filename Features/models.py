from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# model for a calendar event
class CalendarEvent(models.Model):
    """
    Represents a calendar event.

    Attributes:
        title (str): The title of the event.
        startTime (datetime): The start time of the event.
        description (str): The description of the event (optional).
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    start_time = models.DateTimeField() # dang is this all the event needs? feels too simple
    # end-time, whether it repeats, etc to be added later (stretch goal)

    def __str__(self):
        return 'CalendarEvent ' + self.title

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

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'