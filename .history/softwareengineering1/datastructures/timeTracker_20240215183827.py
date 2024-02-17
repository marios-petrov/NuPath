import timeSpent

class timeTracker:
    def __init__(self, categoryName):
        self.categoryName = categoryName
        self.timer = timeSpent.timeSpent(categoryName)
        
        
    def calculateTime(self):
        self.timer.getTimeSpent()
        
    def startTimer(self):
        self.timer.startTimer()
        
    def endTimer(self):
        self.endTimer()

    def getTimeSinceTimerStart(self):
        self.getTimeSinceTimerStart()

    