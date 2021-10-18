class Square:
    """
    The class Square represents a single square in a level.
    A square can contain either an obstacle, coin, goal, enemy or character or it can be empty.
    """
    def __init__(self, is_obstacle=False, is_coin=False, is_enemy=False, is_goal=False):
        """
        Creates a new square which is initially empty.
        Parameter is_obstacle is a boolean value stating whether there is an obstacle in the square or not: boolean.
        Parameter is_coin is a boolean value stating whether there is a coin in the square or not: boolean.
        Parameter is_enemy is a boolean value stating whether there is an enemy in the square or not: boolean.
        Parameter is_goal is a boolean value stating whether there is a goal in the square or not: boolean.
        """
        self.is_obstacle = is_obstacle
        self.is_coin = is_coin
        self.is_enemy = is_enemy
        self.is_goal = is_goal

    def is_obstacle_square(self):
        """
        Returns a boolean value stating whether there is an obstacle in the square or not: boolean.
        """
        return self.is_obstacle

    def is_enemy_square(self):
        """
        Returns a boolean value stating whether there is an enemy in the square or not: boolean.
        """
        return self.is_enemy

    def is_coin_square(self):
        """
        Returns a boolean value stating whether there is a coin in the square or not: boolean.
        """
        return self.is_coin

    def is_goal_square(self):
        """
        Returns a boolean value stating whether there is a goal in the square or not: boolean.
        """
        return self.is_goal

    def is_empty(self):
        """
        Returns a boolean value stating whether the square is empty.
        (A square is empty if it does not contain obstacle, enemy, coin or goal): boolean.
        """
        return not self.is_obstacle_square() and not self.is_enemy_square() and not self.is_coin_square() and not \
            self.is_goal_square()

    def set_obstacle(self):
        """
        Sets an obstacle in this square.
        """
        if self.is_empty():
            self.is_obstacle = True
            return True
        return False

    def set_enemy(self):
        """
        Sets an enemy in this square.
        """
        if self.is_empty():
            self.is_enemy = True
            return True
        return False

    def set_coin(self):
        """
        Sets a coin in this square.
        """
        if self.is_empty():
            self.is_coin = True
            return True
        return False

    def set_goal(self):
        """
        Sets a goal in this square.
        """
        if self.is_empty():
            self.is_goal = True
            return True
        return False

    def remove_coin(self):
        """
        Remove a coin from this square.
        """
        self.is_coin = False
