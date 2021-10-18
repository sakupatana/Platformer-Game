from square import Square


class Level:
    """
    The class Level describes a two dimensional level made up of squares.
    The squares are identified by unique coordinates which range from 0...width-1 and 0...height-1.
    Each square is represented by a Square object.
    Enemies, coins, obstacles, goal, and character can be added to the level.
    """
    def __init__(self, width, height):
        """
        Creates a new level with the specified dimensions. Initially all the squares of the new level are empty.
        """
        # Creates the squares of the level
        self.squares = [None] * width
        for x in range(self.get_width()):
            self.squares[x] = [None] * height
            for y in range(self.get_height()):
                self.squares[x][y] = Square()

        # Save objects into the level
        self.character = None
        self.goal = None
        self.obstacles = []
        self.enemies = []
        self.coins = []

    def get_width(self):
        """
        Returns width of the level in squares: int.
        """
        return len(self.squares)

    def get_height(self):
        """
        Returns the height of the level in squares: int.
        """
        return len(self.squares[0])

    def add_character(self, character, location):
        """
        Adds a new character into the level.
        """
        character.set_level(self, location)
        self.character = character

    def add_obstacle(self, obstacle, location):
        """
        Adds an obstacle at the given location into the level.
        """
        if self.get_square(location).set_obstacle():
            self.obstacles.append(obstacle)
            return True
        return False

    def add_enemy(self, enemy, location):
        """
        Adds an enemy at the given location into the level.
        """
        if self.get_square(location).set_enemy():
            self.enemies.append(enemy)
            return True
        return False

    def add_goal(self, location):
        """
        Adds a goal at the given location into the level.
        """
        goal = self.get_square(location).set_goal()
        self.goal = goal
        return True

    def add_coin(self, coin, location):
        """
        Adds a coin at the given location into the level.
        """
        if self.get_square(location).set_coin():
            self.coins.append(coin)
            return True
        return False

    def get_square(self, coordinates):
        """
        Returns the square that is located at the given location. If the given coordinates point outside of the level,
        this method returns a square that contains an obstacle and is not located in any level.
        """
        if self.contains(coordinates):
            return self.squares[coordinates.get_x()][coordinates.get_y()]
        else:
            return Square(True)

    def contains(self, coordinates):
        """
        Determines if this level contains the given coordinates.
        """
        x_coordinate = coordinates.get_x()
        y_coordinate = coordinates.get_y()
        return 0 <= x_coordinate < self.get_width() and 0 <= y_coordinate < self.get_height()

    def get_coins(self):
        """
        Returns an array containing all the coins currently located in this level: list.
        """
        return self.coins[:]

    def get_enemies(self):
        """
        Returns an array containing all the enemies currently located in this level: list.
        """
        return self.enemies[:]

    def get_obstacles(self):
        """
        Returns an array containing all the obstacles currently located in this level: list.
        """
        return self.obstacles[:]

    def get_character(self):
        """
        Returns the character of the level.
        """
        return self.character
