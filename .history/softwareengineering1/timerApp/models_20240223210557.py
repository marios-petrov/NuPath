#Author Nate Clark

from django.db import models
from django.utils import timezone

class TimeSpent(models.Model):
    """
    Represents a time spent on a timer.

    Attributes:
        timerName (str): The name of the timer.
        startTime (datetime): The start time of the timer.
        endTime (datetime): The end time of the timer.
        currentlyRunning (bool): Indicates whether the timer is currently running.
    """

    timerName = models.CharField(max_length=64)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    currentlyRunning = models.BooleanField(default=False)

    def startTimer(self):
        """
        Starts the timer by setting the currentlyRunning flag to True and updating the start time.
        """
        self.currentlyRunning = True
        self.startTime = timezone.now()
    
    def endTimer(self):
        """
        Ends the timer by setting the currentlyRunning flag to False and updating the end time.
        """
        self.currentlyRunning = False
        self.endTime = timezone.now()

    def getTimeSinceTimerStart(self):
        """
        Calculates the time elapsed since the timer was started.

        Returns:
            timedelta: The time elapsed since the timer was started.
        """
        currentTime = timezone.now()
        if self.currentlyRunning and currentTime <= self.endTime:
            return currentTime - self.endTime

    def getTimeSpent(self):
        """
        Calculates the total time spent on the timer.

        Returns:
            timedelta: The total time spent on the timer.
        
        Raises:
            ValueError: If the timer is still running or if the start time is after the end time.
        """
        if self.startTime <= self.endTime and not self.currentlyRunning:
            return self.endTime - self.startTime
        elif self.startTime <= self.endTime and not self.currentlyRunning:
            return timezone.now() - self.startTime
        else:
            raise ValueError("ERROR: timeSpent.py getTimeSpent not possible time error")
        
    def resetTimer(self):
        """
        Resets the timer by setting the currentlyRunning flag to False and clearing the start and end times.
        """
        self.currentlyRunning = False
        self.startTime = None
        self.endTime = None

        
class TimeTracker(models.Model):
    """
    Represents a time tracker for a specific category.
    """

    categoryName = models.CharField(max_length=64)
    timer = models.ForeignKey(TimeSpent, on_delete=models.CASCADE)
    
    def calculateTime(self):
        """
        Calculates the total time spent for the time tracker.
        
        Returns:
            The total time spent in seconds.
        """
        return self.timer.getTimeSpent()
        
    def startTimer(self):
        """
        Starts the timer for the time tracker.
        
        Returns:
            None
        """
        return self.timer.startTimer()
        
    def endTimer(self):
        """
        Ends the timer for the time tracker.
        
        Returns:
            None
        """
        return self.timer.endTimer()

    def getTimeSinceTimerStart(self):
        """
        Calculates the time elapsed since the timer was started.
        
        Returns:
            The time elapsed in seconds.
        """
        return self.timer.getTimeSinceTimerStart()