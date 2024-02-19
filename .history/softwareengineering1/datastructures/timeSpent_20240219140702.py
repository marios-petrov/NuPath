from django.db import models
from django.utils import timezone

class TimeSpent(models.Model):
    timerName = models.CharField(max_length=64)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    currentlyRunning = models.BooleanField(default=False)

    def startTimer(self):
        self.currentlyRunning = True
        self.startTime = timezone.now()
    
    def endTimer(self):
        self.currentlyRunning = False
        self.endTime = timezone.now()

    def getTimeSinceTimerStart(self):
        currentTime = timezone.now()
        if self.currentlyRunning and currentTime <= self.endTime:
            return currentTime - self.endTime

    def getTimeSpent(self):
        if self.startTime <= self.endTime and not self.currentlyRunning:
            return self.endTime - self.startTime
        elif self.startTime <= self.endTime and not self.currentlyRunning:
            return timezone.now() - self.startTime
        else:
            raise ValueError("ERROR: timeSpent.py getTimeSpent not possible time error")
