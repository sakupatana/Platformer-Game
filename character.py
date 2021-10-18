from coordinates import Coordinates
from square import Square


class Character:
    """
    This class creates new character for the level.
    """
    def __init__(self, name):
        self.name = name
        self.location = None
        self.level = None
        self.graphics_item = None

    def get_name(self):
        """
        Returns the character name : string.
        """
        return self.name

    def get_level(self):
        """
        Returns the level in which the character is.
        """
        return self.level

    def get_location(self):
        """
        Returns the current location of the character in the level.
        """
        return self.location

    def set_graphics_item(self, item):
        """
        Set the created graphics item for the character.
        """
        self.graphics_item = item

    def set_level(self, level, location):
        """
        Places the character in the given level at the specified coordinates.
        """
        self.level = level
        self.location = location

    def set_location(self, location):
        """
        Sets the character location in the given location.
        """
        self.location = location

    def try_move(self, x, y):
        """
        Moves the character in the level if it is possible.
        """
        new_location = Coordinates(x, y)
        new_square = self.level.get_square(new_location)
        # Check if the coordinate includes an obstacle and if it is inside the level
        if not Square.is_obstacle_square(new_square) and self.level.contains(new_location):
            self.location = new_location
            self.graphics_item.update_position()
            return True
