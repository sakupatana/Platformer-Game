

class Coordinates:
    """
    This class represents pairs of integers that specify locations on a two-dimensional grid (level).
    """
    def __init__(self, x, y):
        """
        Creates a new coordinate pair.
        """
        self.x = x
        self.y = y

    def get_x(self):
        """
        Returns the x coordinate: int.
        """
        return self.x

    def get_y(self):
        """
        Returns the y coordinate: int.
        """
        return self.y
