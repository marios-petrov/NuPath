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
    description = models.TextField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    collegeClass = models.ForeignKey(CollegeClass, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class CollegeClass(models.Model):
    class_name = models.CharField(max_length=64)
    calendar_event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    class_description = models.TextField(blank=True)
