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

class Doodle(models.Model):
    image = models.ImageField(upload_to='doodles/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doodle {self.id} by {self.user.username}"
