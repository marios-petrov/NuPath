from django.db import models
class CalendarEvent(models.Model):
    title = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
