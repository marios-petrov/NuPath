
from django.db import models

class TodoList(models.Model):
    name = models.CharField(max_length=64)

class TodoItem(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    todo_list = models.ForeignKey(TodoList, related_name='items', on_delete=models.CASCADE)

    def is_complete(self):
        return self.completed
    
    def mark_complete(self):
        self.completed = True
        self.save()

    def mark_not_complete(self):
        self.completed = False
        self.save()