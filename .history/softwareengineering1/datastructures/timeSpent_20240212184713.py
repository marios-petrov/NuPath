import time

class timeSpent:
    def __init__(self, timerName):
        self.timerName = timerName
        startTime = 0
        endTime = 0
        currentlyRunning = False


    def startTimer(self):
        startTime = time.time()
    
    def endTimer(self):
        endTime = time.time()

    def getTimeSinceTimerStart():
        currentTime = time.time()
        if (currentlyRunning & currentTime <= self.endTime):
            return currentTime - self.endTime


    def getTimeSpent(self):
        if (self.startTime <= self.endTime):
            return self.endTime - self.startTime
        else:
            return "Timer not ended or started incorrectly"