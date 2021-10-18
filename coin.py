from coordinates import Coordinates


class Coin:
    """
    This class creates new coin objects that can be added to a level.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Set a value for the coin
        self.value = 1

    def get_location(self):
        """
        Returns the location of coin.
        """
        x = self.x
        y = self.y
        location = Coordinates(x, y)
        return location

    def get_value(self):
        """
        Returns the value of coin.
        """
        return self.value

