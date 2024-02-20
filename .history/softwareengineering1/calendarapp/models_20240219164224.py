from django.db import models

# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length=64)
    group_description = models.TextField(blank=True)

    def __str__(self):
        return self.group_name

class CalendarEvent(models.Model):
    title = models.CharField(max_length=64)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField(blank=True, default="")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, default='')

    def __str__(self):
        return self.title


