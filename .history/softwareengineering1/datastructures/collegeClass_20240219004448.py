from django.db import models
from calendarEvent import CalendarEvent

class CollegeClass(models.Model):
    class_name = models.CharField(max_length=255)
    calendar_event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    class_description = models.TextField(blank=True)
