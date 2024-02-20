from django.db import models
from .timeSpent import TimeSpent

class TimeTracker(models.Model):
    categoryName = models.CharField(max_length=64)
    timer = models.ForeignKey(TimeSpent, on_delete=models.CASCADE)
    
    def calculateTime(self):
        return self.timer.getTimeSpent()
        
    def startTimer(self):
        return self.timer.startTimer()
        
    def endTimer(self):
        return self.timer.endTimer()

    def getTimeSinceTimerStart(self):
        return self.timer.getTimeSinceTimerStart()
