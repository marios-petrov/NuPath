#Author Nate Clark

from django.db import models

# Create your models here.
class CalendarGroup(models.Model):
    """
    Represents a group in the calendar app.

    Attributes:
        group_name (str): The name of the group.
        group_type (str): The type of the group.
        group_description (str): The description of the group (optional).
    """
    group_name = models.CharField(max_length=64)
    group_type = models.CharField(max_length=64)
    group_description = models.TextField(blank=True)

    def __str__(self):
        return self.group_name

class CalendarEvent(models.Model):
    """
    Represents a calendar event.

    Attributes:
        title (str): The title of the event.
        startTime (datetime): The start time of the event.
        endTime (datetime): The end time of the event.
        description (str): The description of the event (optional).
    """
    title = models.CharField(max_length=64)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return 'Group: ' + self.group.group_name + ' Title: ' + self.title


