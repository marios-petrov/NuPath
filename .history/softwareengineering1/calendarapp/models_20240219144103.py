from django.db import models

# Create your models here.
class CalendarEvent(models.Model):
    title = models.CharField(max_length=64)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class CollegeClass(models.Model):
    class_name = models.CharField(max_length=64)
    calendar_event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    class_description = models.TextField(blank=True)
