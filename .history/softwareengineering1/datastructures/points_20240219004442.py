from django.db import models
class PointsCounter(models.Model):
    points = models.IntegerField(default=0)

    def add_points(self, amount):
        if amount > 0:
            self.points += amount
            self.save()

    def remove_points(self, amount):
        if amount > 0 and self.points >= amount:
            self.points -= amount
            self.save()

    def clear_points(self):
        self.points = 0
        self.save()
