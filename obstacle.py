from coordinates import Coordinates


class Obstacle:
    """
    This class creates new obstacle objects that can be added to a level.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_location(self):
        """
        Returns the location of the obstacle.
        """
        x = self.x
        y = self.y
        location = Coordinates(x, y)
        return location
