from django.db import models
from django.contrib.auth.models import User


# Create your models here.

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
