class PointsCounter:
    def __init__(self):
        self.points = 0

    def add_points(self, amount):
        if amount > 0:
            self.points += amount

    def remove_points(self, amount):
        if amount > 0 and self.points >= amount:
            self.points -= amount

    def clear_points(self):
        self.points = 0