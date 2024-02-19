from django.db import models
class TodoItem(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def is_complete(self):
        return self.completed
    
    def mark_complete(self):
        self.completed = True

    def mark_not_complete(self):
        self.completed = False