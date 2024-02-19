from django.db import models

# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def is_complete(self):
        return self.completed
    
    def mark_complete(self):
        self.completed = True
        self.save()

    def mark_not_complete(self):
        self.completed = False
        self.save()
        
class TodoList(models.Model):
    name = models.CharField(max_length=64)
    categoryName = models.CharField(max_length=64)
