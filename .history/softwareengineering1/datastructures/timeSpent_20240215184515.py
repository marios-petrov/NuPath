import time

class timeSpent:
    def __init__(self, timerName):
        self.timerName = timerName
        startTime = 0
        endTime = 0
        currentlyRunning = False


    def startTimer(self):
        currentlyRunning = True
        startTime = time.time()
    
    def endTimer(self):
        currentlyRunning = False
        endTime = time.time()

    def getTimeSinceTimerStart():
        currentTime = time.time()
        if (currentlyRunning & currentTime <= self.endTime):
            return currentTime - self.endTime


    def getTimeSpent(self):
        if (self.startTime <= self.endTime & self.currentlyRunning == False):
            return self.endTime - self.startTime
        elif (self.startTime <= self.endTime):
            return time.time() - self.startTime
        else:
            print("ERROR: timeSpent.py getTimeSpent not possible time error")
            return 0 #error