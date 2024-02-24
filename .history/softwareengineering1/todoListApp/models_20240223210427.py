#Author Nate Clark

from django.db import models

class TodoItem(models.Model):
    """
    Represents a todo item in the todo list.

    Attributes:
        title (str): The title of the todo item
        description (str): The description of the event (optional).
        completed (bool): True if the todo item is complete, False otherwise.
    """

    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def is_complete(self):
        """
        Checks if the todo item is complete.

        Returns:
            bool: True if the todo item is complete, False otherwise.
        """
        return self.completed
    
    def mark_complete(self):
        """
        Marks the todo item as complete.
        """
        self.completed = True
        self.save()

    def mark_not_complete(self):
        """
        Marks the todo item as not complete.
        """
        self.completed = False
        self.save()
        
class TodoList(models.Model):
    """
    Represents a todo list.

    Attributes:
        name (str): The name of the todo list.
        categoryName (str): The category name of the todo list.
    """
    name = models.CharField(max_length=64)
    categoryName = models.CharField(max_length=64)

class PointsCounter(models.Model):
    """
    A model representing a points counter.

    Attributes:
        points (int): The current number of points.

    Methods:
        add_points(amount): Adds the specified amount of points to the counter.
        remove_points(amount): Removes the specified amount of points from the counter.
        clear_points(): Resets the counter to zero.
    """

    points = models.IntegerField(default=0)

    def add_points(self, amount):
        """
        Adds the specified amount of points to the counter.

        Args:
            amount (int): The number of points to add.

        Returns:
            None
        """
        if amount > 0:
            self.points += amount
            self.save()

    def remove_points(self, amount):
        """
        Removes the specified amount of points from the counter.

        Args:
            amount (int): The number of points to remove.

        Returns:
            None
        """
        if amount > 0 and self.points >= amount:
            self.points -= amount
            self.save()

    def clear_points(self):
        """
        Resets the counter to zero.

        Returns:
            None
        """
        self.points = 0
        self.save()
