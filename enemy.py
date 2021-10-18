from coordinates import Coordinates


class Enemy:
    """
    This class creates new enemy objects that can be added to a level.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_location(self):
        """
        Returns the location of the enemy.
        """
        x = self.x
        y = self.y
        location = Coordinates(x, y)
        return location
