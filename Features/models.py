from django.db import models

# Create your models here.

# model for a calendar event
class CalendarEvent(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	start_time = models.DateTimeField()
	# end-time, whether it repeats, etc to be added later (stretch goal)