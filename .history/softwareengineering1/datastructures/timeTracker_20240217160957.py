import timeSpent

class timeTracker:
    def __init__(self, categoryName):
        self.categoryName = categoryName
        self.timer = timeSpent.timeSpent(categoryName)
        self.activities = []
        
    def addActivity(self, activity):
        self.activities.append(activity)
        
    def calculateTotalTime(self):
        total_time = 0
        for activity in self.activities:
            total_time += activity.getTimeSpent()
        return total_time
        
    def startTimer(self):
        self.timer.startTimer()
        
    def endTimer(self):
        self.timer.endTimer()

    def getTimeSinceTimerStart(self):
        return self.timer.getTimeSinceTimerStart()
