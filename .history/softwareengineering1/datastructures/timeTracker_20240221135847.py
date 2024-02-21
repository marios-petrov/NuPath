import timeSpent
import datetime

class timeTracker:
    def __init__(self, categoryName):
        self.categoryName = categoryName
        self.timer = timeSpent.timeSpent(categoryName)
        self.pastTimers = list()
        
        
    def calculateTime(self, date):
        self.timer.getTimeSpent()
        
    def startTimer(self):
        self.timer.startTimer()
        
    def endTimer(self):
        time = self.endTimer()
        if (time != 0):
            self.pastTimers.insert([datetime.date(), time])

    def getTimeSinceTimerStart(self):
        return self.getTimeSinceTimerStart()

    def getTimeInMinutes(self):
        return self.getTimeInMinutes / 60