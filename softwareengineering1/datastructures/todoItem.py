class todoItem:
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.completed = False

    def isComplete(self):
        return self.completed
    
    def markComplete(self):
        self.completed = True

    def markNotComplete(self):
        self.completed = False