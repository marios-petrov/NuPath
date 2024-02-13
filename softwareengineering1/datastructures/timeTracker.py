import timeSpent

class timeTracker:
    def __init__(self, categoryName):
        self.categoryName = categoryName
        self.timer = list(timeSpent(categoryName))