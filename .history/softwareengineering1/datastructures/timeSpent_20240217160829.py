import time

class TimeSpent:
    def __init__(self, timerName):
        self.timerName = timerName
        self.startTime = 0
        self.endTime = 0
        self.currentlyRunning = False

    def startTimer(self):
        self.currentlyRunning = True
        self.startTime = time.time()
    
    def endTimer(self):
        self.currentlyRunning = False
        self.endTime = time.time()

    def getTimeSinceTimerStart(self):
        currentTime = time.time()
        if self.currentlyRunning and currentTime <= self.endTime:
            return currentTime - self.endTime

    def getTimeSpent(self):
        if self.startTime <= self.endTime and not self.currentlyRunning:
            return self.endTime - self.startTime
        elif self.startTime <= self.endTime:
            return time.time() - self.startTime
        else:
            raise ValueError("ERROR: timeSpent.py getTimeSpent not possible time error")
