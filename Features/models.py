from django.db import models

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