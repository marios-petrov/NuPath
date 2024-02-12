import todoItem

class todoList:
    def __init__(self):
        self.todoList = []

    def addToDoItem(self, title, description=""):
        self.todoList.append(todoItem(title, description))