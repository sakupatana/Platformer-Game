"""
PLATFORMER GAME
Saku Patana
Programming Y2
Aalto University
"""
import sys
from os import path
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtWidgets import *

from level import Level
from coordinates import Coordinates
from character import Character
from enemy import Enemy
from coin import Coin
from obstacle import Obstacle
from enemy_graphics_item import EnemyGraphicsItem
from character_graphics_item import CharacterGraphicsItem
from coin_graphics_item import CoinGraphicsItem
from obstacle_graphics_item import ObstacleGraphicsItem

# Contents
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Platformer"
SQUARE_SIZE = 30

# The colors used in the game
GREEN = QColor(0, 255, 0)
BLACK = QColor(0, 0, 0)
GREY = QColor(211, 211, 211)
BLUE = QColor(0, 0, 128)
RED = QColor(255, 0, 0)
YELLOW = QColor(255, 255, 0)
SKY = QColor(50, 200, 250)

# Values that are used in character movements
PLAYER_SPEED = 1
PLAYER_JUMP_HEIGHT = 2
GRAVITY = 1
SPEED = 100
START_LOCATION_X = 1
START_LOCATION_Y = 18

# The files used to save the results for each level
RESULTS_FILE_LV1 = "results_lv1.txt"
RESULTS_FILE_LV2 = "results_lv2.txt"
RESULTS_FILE_LV3 = "results_lv3.txt"


class GameGUI(QMainWindow):
    """
    The class GUI handles the drawing of a game and allows user to interact with it.
    """
    def __init__(self, square_size):
        super().__init__()
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.horizontal = QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)

        # Variables used to manage the game
        self.game = None
        self.character = None
        self.character_graphics_item = None
        self.square_size = square_size
        self.score = 0
        self.level = 1
        self.jump_height = 0
        self.jump = False
        self.gravity = False
        self.stopped = False
        self.lv2_finished = False
        self.first_level = None
        self.second_level = None
        self.third_level = None

        # Lists of objects that are in the game
        self.added_enemies = []
        self.added_coins = []
        self.added_obstacles = []
        self.added_coin_items = []
        self.added_enemy_items = []
        self.added_obstacle_items = []

        # Timer for the game to control movements
        self.timer = QBasicTimer()
        self.timer.start(SPEED, self)
        # Load the file where the results are saved
        self.load_results()
        # Create the levels of the game
        self.create_levels()
        # Create the window
        self.init_window()

        # Draw the level and the objects in the scene
        self.add_level_grid_items()
        self.add_enemy_graphics_items()
        self.add_coin_graphics_items()
        self.add_obstacle_graphics_items()
        # Create, add and draw the character
        self.create_character()
        self.add_character_graphics_item()

# METHODS TO SET UP THE GAME -------------------------------------------------------------------------------------------

    def load_results(self):
        """
        Loads the file where the results are saved.
        """
        self.dir = path.dirname(__file__)
        # Load this file if the level is 1
        if self.level == 1:
            with open(path.join(self.dir, RESULTS_FILE_LV1), "r") as file:
               self.results = file.read()

        # Load this file if the level is 2
        if self.level == 2:
            with open(path.join(self.dir, RESULTS_FILE_LV2), "r") as file:
                self.results = file.read()

        # Load this file if the level is 3
        if self.level == 3:
            with open(path.join(self.dir, RESULTS_FILE_LV3), "r") as file:
                self.results = file.read()

    def init_window(self):
        """
        Sets up the window.
        """
        self.setGeometry(400, 100, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.setWindowTitle(SCREEN_TITLE)
        # Disable the maximize button of the main window
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        # Restart the level button
        self.reset_game = QPushButton("Restart the level", self)
        self.reset_game.setGeometry(200, 38, 200, 50)
        self.reset_game.setStyleSheet("background-color: grey")
        self.reset_game.setFont(QFont('Times', 12))
        self.reset_game.clicked.connect(self.reset_level)

        # Exit the game button
        self.exit_game = QPushButton("Exit the game", self)
        self.exit_game.setGeometry(500, 38, 200, 50)
        self.exit_game.setStyleSheet("background-color: grey")
        self.exit_game.setFont(QFont('Times', 12))
        self.exit_game.clicked.connect(self.leave_game)

        # Next level button
        self.next_level = QPushButton("Next level", self)
        self.next_level.setGeometry(600, 100, 100, 60)
        self.next_level.setStyleSheet("background-color: green")
        self.next_level.setFont(QFont('Times', 12))
        self.next_level.clicked.connect(lambda: self.change_level(self.next_level))
        # The button is hidden before the player win the first level
        self.next_level.setVisible(False)

        # Previous level button
        self.previous_level = QPushButton("Previous level", self)
        self.previous_level.setGeometry(730, 100, 130, 60)
        self.previous_level.setStyleSheet("background-color: grey")
        self.previous_level.setFont(QFont('Times', 12))
        self.previous_level.clicked.connect(lambda: self.change_level(self.previous_level))
        # The button is hidden before the player move to the second level
        self.previous_level.setVisible(False)

        # Text to tell the result of the game
        self.result = QLabel(self)
        self.result.setGeometry(325, 100, 260, 60)
        self.result.setStyleSheet("QLabel" "{" "border : 3px solid black;" "background : white;" "}")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setFont(QFont('Times', 15))

        # Text to tell that game has reached the end
        self.end_result = QLabel(self)
        self.end_result.setGeometry(200, 300, 500, 200)
        self.end_result.setStyleSheet("QLabel" "{" "border : 3px solid black;" "background : green;" "}")
        self.end_result.setText("Congratulations! You have successfully passed all the levels of the game")
        self.end_result.setWordWrap(True)
        self.end_result.setAlignment(Qt.AlignCenter)
        self.end_result.setFont(QFont('Times', 20))
        self.end_result.setVisible(False)

        # The result board that collects the top scores of the game
        self.top_scores = QLabel(f"TOP SCORES:\n{self.results}", self)
        self.top_scores.setGeometry(20, 300, 125, 245)
        self.top_scores.setStyleSheet("QLabel" "{" "border : 3px solid black;" "background : white;" "}")
        self.top_scores.setWordWrap(True)
        self.top_scores.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.top_scores.setFont(QFont('Times', 10))

        # Visualizing the score during the game
        self.score_text = QLabel(f"Score: {self.score}", self)
        self.score_text.move(30, 200)
        self.score_text.setStyleSheet("QLabel" "{" "border : 3px solid black;" "background : white;" "}")
        self.score_text.resize(100, 50)
        self.score_text.setAlignment(Qt.AlignCenter)
        self.score_text.setFont(QFont('Times', 12))

        # Visualizing the level during the game
        self.level_text = QLabel(f"Level: {self.level}", self)
        self.level_text.move(150, 140)
        self.level_text.resize(100, 30)
        self.level_text.setAlignment(Qt.AlignCenter)
        self.level_text.setFont(QFont('Times', 14))

        # Visualizing the game instructions
        self.instructions = QLabel(self)
        self.instructions.move(30, 790)
        self.instructions.resize(250, 90)
        self.instructions.setStyleSheet("QLabel" "{" "border : 1px solid black;" "}")
        self.instructions.setText("INSTRUCTIONS TO PLAY THE GAME:\n Jump = W    :    Down = S \n Right = D     :"
                                  "    Left = A \n Exit = Esc     :    Restart = R")
        self.instructions.setWordWrap(True)
        self.instructions.setAlignment(Qt.AlignLeft)
        self.instructions.setFont(QFont('Times', 8))

        # Visualizing the game rules
        self.rules = QLabel(self)
        self.rules.move(300, 785)
        self.rules.resize(570, 100)
        self.rules.setStyleSheet("QLabel" "{" "border : 1px solid black;" "}")
        self.rules.setText("RULES OF THE GAME: \n - Try to move the character (blue box) to the goal (black box) and "
                           "collecting as many coins (yellow circles) as possible without colliding with the enemies "
                           "(red triangles) \n - If you collide with a coin, you get 1 point which you can monitor in "
                           "Score-box \n - If you collide with an enemy, you lose the game \n - If you collide with "
                           "the goal, you win the game and you have a chance to move to the next level")
        self.rules.setWordWrap(True)
        self.rules.setAlignment(Qt.AlignLeft)
        self.rules.setFont(QFont('Times', 8))

        # Show the main window
        self.show()
        # Add a scene for drawing 2d objects for the level
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(50, 20, 500, 500)
        # Add a view for showing the scene inside the main window
        self.view = QGraphicsView(self.scene)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)

    def create_character(self):
        """
        Creates the character for the game based on the user input.
        """
        # Ask player to give the name
        self.input = QInputDialog()
        self.input.move(500, 200)
        self.input.view = QWidget(self.input)
        self.input.view.setStyleSheet("QInputDialog" "{" "background-color : lightgrey;" "}")
        player_name, ok = self.input.getText(self.input.view, "TO START", "Enter the name of your character:")

        # Check that the name is given and ok button is pressed
        if player_name and ok:
            # Create the character based on the user input
            game_character = Character(player_name)
            character_location = Coordinates(START_LOCATION_X, START_LOCATION_Y)
            self.game.add_character(game_character, character_location)
            self.character = game_character
        # If the input is empty or cancel button is pressed, leave the game
        else:
            self.leave_game()

    def add_character_graphics_item(self):
        """
        Adds QGraphicsItem for a character that can be used throughout the game.
        """
        new_character = CharacterGraphicsItem(self.character, self.square_size, BLUE)
        self.character_graphics_item = new_character
        self.character.set_graphics_item(new_character)
        self.scene.addItem(new_character)

    def add_level_grid_items(self):
        """
        Adds QGraphicsItem for each square in the level, if the square is goal, the color is black.
        """
        # Iterate over all squares in the level
        level_width = self.game.get_width()
        level_height = self.game.get_height()
        for x in range(level_width):
            for y in range(level_height):
                new_rect = QGraphicsRectItem((self.square_size * x), (self.square_size * y), self.square_size,
                                             self.square_size)
                # If the square is goal, the color is black
                if self.game.get_square(Coordinates(x, y)).is_goal_square():
                    new_rect.setBrush(QBrush(BLACK))
                    self.scene.addItem(new_rect)
                # Otherwise the color is sky blue representing empty square
                else:
                    new_rect.setPen(QPen(SKY))
                    new_rect.setBrush(QBrush(SKY))
                    self.scene.addItem(new_rect)

    def add_enemy_graphics_items(self):
        """
        Adds an EnemyGraphicsItem for the enemies of level that have yet not been added to the game.
        If the enemy has a graphics item, it is visualized again in the scene of the game.
        """
        enemies = self.game.get_enemies()
        for enemy in enemies:
            # If the enemy is not in the game, new graphics item is created
            if enemy not in self.added_enemies:
                new_item = EnemyGraphicsItem(enemy, self.square_size, RED)
                self.scene.addItem(new_item)
                self.added_enemy_items.append(new_item)
                self.added_enemies.append(enemy)
            # If the enemy is in the game, its graphics item is visualized in the game
            elif enemy in self.added_enemies:
                items = self.added_enemy_items
                for item in items:
                    if item.get_enemy() == enemy:
                        self.scene.addItem(item)

    def add_coin_graphics_items(self):
        """
        Adds a CoinGraphicsItem for the coins of level that have yet not been added to the game.
        If the coin has a graphics item, it is visualized again in the scene of the game.
        """
        coins = self.game.get_coins()
        for coin in coins:
            # If the coin is not in the game, new graphics item is created
            if coin not in self.added_coins:
                new_item = CoinGraphicsItem(coin, self.square_size, YELLOW)
                self.scene.addItem(new_item)
                self.added_coin_items.append(new_item)
                self.added_coins.append(coin)
            # If the coin is in the game, its graphics item is visualized in the game
            elif coin in self.added_coins:
                items = self.added_coin_items
                for item in items:
                    if item.get_coin() == coin:
                        self.scene.addItem(item)

    def add_obstacle_graphics_items(self):
        """
        Adds an ObstacleGraphicsItem for the obstacles of level that have yet not been added to the game.
        If the obstacle has a graphics item, it is visualized again in the scene of the game.
        """
        obstacles = self.game.get_obstacles()
        for obstacle in obstacles:
            # If the obstacle is not in the game, new graphics item is created
            if obstacle not in self.added_obstacles:
                new_item = ObstacleGraphicsItem(obstacle, self.square_size, GREEN)
                self.scene.addItem(new_item)
                self.added_obstacle_items.append(new_item)
                self.added_obstacles.append(obstacle)
            # If the obstacle is in the game, its graphics item is visualized in the game
            elif obstacle in self.added_obstacles:
                items = self.added_obstacle_items
                for item in items:
                    if item.get_obstacle() == obstacle:
                        self.scene.addItem(item)

# METHODS TO MANAGE THE GAME DURING USER INTERACTION -------------------------------------------------------------------

    def keyPressEvent(self, event):
        """
        Called when the user press a key.
        """
        key = event.key()
        # Check if the game is stopped
        if not self.stopped:

            # Get the current location of the character
            location = self.character.get_location()
            x = Coordinates.get_x(location)
            y = Coordinates.get_y(location)

            # Handle the key presses
            # If the event is W the character moves up by jumping
            if key == Qt.Key_W:
                # If gravity is activated, jump event is ignored
                if self.gravity:
                    event.ignore()
                else:
                    self.jump = True
            # If the event is S the character moves down by player speed
            elif key == Qt.Key_S:
                self.character.try_move(x, (y + PLAYER_SPEED))
            # If the event is D, the character moves right by player speed
            elif key == Qt.Key_D:
                self.character.try_move((x + PLAYER_SPEED), y)
            # If the event is A, the character moves left by player speed
            elif key == Qt.Key_A:
                self.character.try_move((x - PLAYER_SPEED), y)
            # If the event is Escape, the game ends and exits from the application
            elif key == Qt.Key_Escape:
                self.leave_game()
            # If the event is R during the game, the level is restarted
            elif key == Qt.Key_R:
                self.reset_level()

            # Add gravity to the game if jump is not active
            if not self.jump:
                self.gravity = True

            # Check for collision with the other objects
            self.check_collision()

        # These buttons can be pressed although the game is stopped
        elif key == Qt.Key_Escape:
            self.leave_game()
        elif key == Qt.Key_R:
            self.reset_level()
        # Otherwise ignore the event if game is stopped
        else:
            event.ignore()

    def timerEvent(self, event):
        """
        Refreshes the gravity and jumping according the time set in timer (SPEED).
        """
        # If self.jump is False, gravity is activated and if it is True, jumping is activated
        self.gravity_activate()
        if self.jump:
            self.jumping()

    def jumping(self):
        """
        Called to handle the jumping of the character.
        """
        if self.jump:
            # Get the current location
            location = self.character.get_location()
            x = Coordinates.get_x(location)
            y = Coordinates.get_y(location)

            # Check collision during jumping
            self.check_collision()

            # Move the character always player_speed up until maximum jump height is reached
            move = self.character.try_move(x, (y - PLAYER_SPEED))
            if move and self.jump_height <= PLAYER_JUMP_HEIGHT:
                self.jump_height += 1
            else:
                # End jumping and start gravity when maximum height is reached
                self.jump = False
                self.gravity = True
                # Reset jump_height to zero when jumping is deactivated
                self.jump_height = 0

    def gravity_activate(self):
        """
        Called to handle the gravity of the level.
        """
        if self.gravity:
            # Get the current location of the character
            location = self.character.get_location()
            x = Coordinates.get_x(location)
            y = Coordinates.get_y(location)

            # Check collision during gravity
            self.check_collision()

            # Move the character always according to gravity down until an obstacle is below
            move = self.character.try_move(x, (y + GRAVITY))
            if not move:
                # End gravity when obstacle is below
                self.gravity = False

    def check_collision(self):
        """
        Called to check collision during the game.
        """
        # Check collision with coins
        self.check_coin_collision()

        # Check collision with enemies
        is_enemy = self.check_enemy_collision()
        if is_enemy:
            game_over = -1
            # Check result after colliding with the enemy
            self.check_result(game_over)

        # Check collision with goal
        is_goal = self.check_goal_collision()
        if is_goal:
            game_over = 1
            # Check result after colliding with the goal
            self.check_result(game_over)

    def check_coin_collision(self):
        """
        Called to check if collision with a coin is detected.
        """
        location = self.character.get_location()
        x = Coordinates.get_x(location)
        y = Coordinates.get_y(location)
        # Check if collision is detected
        if self.game.get_square(location).is_coin_square():
            coins = self.added_coins
            # Remove the coin from the coin list and scene after collision
            for i, coin in enumerate(coins):
                coin_location = coin.get_location()
                x2 = Coordinates.get_x(coin_location)
                y2 = Coordinates.get_y(coin_location)
                if x == x2 and y == y2:
                    for coin_item in self.added_coin_items:
                        item = coin_item.get_coin()
                        if coin == item:
                            # Remove the collected coin from scene and list of the coins
                            square = self.game.get_square(coin_location)
                            square.remove_coin()
                            self.scene.removeItem(coin_item)
                            del coins[i]
                            # Score is updated
                            value = coin.get_value()
                            self.score += value
                            self.score_text.setText(f"Score: {self.score}")
            return True

    def check_enemy_collision(self):
        """
        Called to check if collision with an enemy is detected.
        """
        location = self.character.get_location()
        if self.game.get_square(location).is_enemy_square():
            # Remove the character graphics item from the scene
            self.scene.removeItem(self.character_graphics_item)
            # Stop the game so that moves cannot be made
            self.stopped = True
            return True

    def check_goal_collision(self):
        """
        Called to check if collision with the goal is detected.
        """
        location = self.character.get_location()
        if self.game.get_square(location).is_goal_square():
            # Remove the character graphics item from the scene
            self.scene.removeItem(self.character_graphics_item)
            # Stop the game so that moves cannot be made
            self.stopped = True
            return True

    def check_result(self, game_over):
        """
        Called to check the result of the game.
        """
        # Stop the timer so that moves cannot be made
        self.timer.stop()

        # Check if the player has lost
        if game_over == -1:
            # Visualizes that the player has lost
            self.result.setText("You have lost")
            self.result.setStyleSheet("QLabel" "{" "border : 3px solid black;" "background : red;" "}")

        # Check if the player has won
        if game_over == 1:
            # Visualizes that the player has won
            self.result.setText("You have won")
            self.result.setStyleSheet("QLabel" "{" "border : 3px solid black;" "background : green;" "}")

            # Check what is the current level
            if self.level == 1:
                # Set the next level button now visible
                self.next_level.setVisible(True)
                # Update the results in the file of level 1
                self.update_results(RESULTS_FILE_LV1)

            if self.level == 2:
                # Set the next level button now visible
                self.next_level.setVisible(True)
                # Update the results in the file of level 2
                self.update_results(RESULTS_FILE_LV2)
                # Set level 2 as finished so that next level button can be managed later
                self.lv2_finished = True

            if self.level == 3:
                # Set the next level button now visible
                self.next_level.setVisible(False)
                # Update the results in the file of level 3
                self.update_results(RESULTS_FILE_LV3)
                # Set the end result text visible after last level
                self.end_result.setVisible(True)

    def update_results(self, result_file):
        """
        Called to update the new result into the file corresponding to the level.
        """
        # Write the result in the file where scores are saved
        with open(path.join(self.dir, result_file), "a") as file:
            file.write("{} : {}\n".format(self.character.get_name(), self.score))

        # Read the file so that updated scores can be sorted
        with open(path.join(self.dir, result_file), "r+") as file:
            lines = file.readlines()
            # Add the results in a list
            list_results = []
            for line in lines:
                if line == "\n":
                    continue
                result = line.rstrip("\n")
                list_results.append(result)
            # Sort the results according to the score
            sorted_results = sorted(list_results, key=lambda x: x[-1], reverse=True)
            # Add sorted results in the file
            file.seek(0, 0)
            for result in sorted_results:
                file.write("{}\n".format(result))

        # Open the sorted file
        with open(path.join(self.dir, result_file), "r") as file:
            self.results = file.read()

        # Update the results according to the sorted file
        self.top_scores.setText(f"TOP SCORES:\n{self.results}")

    def leave_game(self):
        """
        Called when the exit button is pressed to exit from the app.
        """
        sys.exit()

    def reset_level(self):
        """
        Called when the restart button is pressed to reset the current level.
        """
        # Change stopped from True to False so moves can be made again
        self.stopped = False
        # Start the timer so that gravity and jumping work again
        self.timer.start(SPEED, self)

        # Reset character location and graphics item
        start_location = Coordinates(START_LOCATION_X, START_LOCATION_Y)
        self.character.set_location(start_location)
        self.scene.addItem(self.character_graphics_item)
        self.character_graphics_item.update_position()

        # Reset the score board
        self.score = 0
        self.score_text.setText(f"Score: {self.score}")
        # Reset the coins
        self.reset_coins()

        # Reset the game result board
        self.result.setText("")
        self.result.setStyleSheet("QLabel" "{" "border : 3px solid black;" "background : white;" "}")
        self.end_result.setVisible(False)

    def reset_coins(self):
        """
        Called to reset the coins that have been collected from the level.
        """
        game_coins = self.added_coins
        level_coins = self.game.get_coins()
        coin_items = self.added_coin_items
        # Check if the coin of the level is not in the list of coins of the game
        for coin in level_coins:
            if coin not in game_coins:
                for coin_item in coin_items:
                    if coin_item.get_coin() == coin:
                        # Add the coin back to the list of coins and scene
                        location = coin.get_location()
                        square = self.game.get_square(location)
                        square.set_coin()
                        self.scene.addItem(coin_item)
                        self.added_coins.append(coin)

    def change_level(self, button):
        """
        Called when the next level or previous level button is pressed to set the level.
        """
        # Change stopped from True to False so moves can be made again
        self.stopped = False
        # Start the timer so that gravity and jumping work again
        self.timer.start(SPEED, self)

        # Reset coins that have been collected before removing so that all are removed
        self.reset_coins()
        # Remove the coin objects from the scene
        for coin_item in self.added_coin_items:
            self.scene.removeItem(coin_item)
        # Remove the enemy objects from the scene
        for enemy_item in self.added_enemy_items:
            self.scene.removeItem(enemy_item)
        # Remove the obstacle objects from the scene
        for obstacle_item in self.added_obstacle_items:
            self.scene.removeItem(obstacle_item)

        # Update variables
        self.score = 0
        # Check if the next level button is pressed
        if button == self.next_level:
            self.level += 1
            # Check if level 2 is finished and current level is 2 so that next level button can be pressed
            if self.lv2_finished and self.level == 2:
                self.previous_level.setVisible(True)
                self.next_level.setVisible(True)
            # Otherwise next_level button is not visible
            else:
                self.previous_level.setVisible(True)
                self.next_level.setVisible(False)
        # Check if the previous level button is pressed
        if button == self.previous_level:
            self.level -= 1
            # Check if current level is 1 so that previous level button cannot be pressed
            if self.level == 1:
                self.previous_level.setVisible(False)
                self.next_level.setVisible(True)
            # Otherwise previous_level button is visible
            else:
                self.next_level.setVisible(True)
                self.previous_level.setVisible(True)

        # Define which level is created according to the level number
        if self.level == 1:
            self.game = self.first_level
        if self.level == 2:
            self.game = self.second_level
        if self.level == 3:
            self.game = self.third_level

        # Crate the graphics items according to the level
        self.add_level_grid_items()
        self.add_enemy_graphics_items()
        self.add_coin_graphics_items()
        self.add_obstacle_graphics_items()

        # Reset character's level and location
        self.scene.removeItem(self.character_graphics_item)
        start_location = Coordinates(START_LOCATION_X, START_LOCATION_Y)
        self.character.set_level(self.game, start_location)
        # Add the character into to level if it has not been done yet
        if self.game.get_character() is None:
            self.game.add_character(self.character, start_location)
        self.scene.addItem(self.character_graphics_item)
        self.character_graphics_item.update_position()

        # Reset the labels of the game
        self.result.setText("")
        self.result.setStyleSheet("QLabel" "{" "border : 3px solid black;" "background : white;" "}")
        self.level_text.setText(f"Level: {self.level}")
        self.score_text.setText(f"Score: {self.score}")
        self.end_result.setVisible(False)

        # Update the top scores according to the level
        self.load_results()
        self.top_scores.setText(f"TOP SCORES:\n{self.results}")

    def create_levels(self):
        """
        Set up the levels of the game so that they can be used later during the game.
        """
        # Set up the first level
        self.first_level = Level(20, 20)
        # Make the first level to be the level of the game that is visualized first
        self.game = self.first_level

        # Set up the obstacles for first level
        coordinate_list = [
            [0, 19], [1, 19], [2, 19], [3, 19], [4, 19], [5, 19], [6, 19], [7, 19], [8, 19], [9, 19], [10, 19],
            [11, 19], [12, 19], [13, 19], [14, 19], [15, 19], [16, 19], [17, 19], [18, 19], [19, 19], [8, 18],
            [9, 18], [9, 17], [9, 18], [15, 16], [14, 15], [13, 14], [12, 14], [12, 13], [12, 12], [12, 11],
            [11, 11], [8, 11], [7, 11], [6, 11], [4, 9], [3, 9], [2, 9], [1, 9], [1, 6], [4, 4], [5, 4], [6, 5],
            [7, 5], [8, 5], [9, 5], [11, 6], [12, 7], [13, 7], [14, 7], [15, 7], [16, 7], [17, 7], [17, 6], [17, 5],
            [17, 4], [18, 3], [19, 3]
        ]
        for coordinate in coordinate_list:
            x = coordinate[0]
            y = coordinate[1]
            game_obstacle = Obstacle(x, y)
            obstacle_location = Coordinates(x, y)
            self.first_level.add_obstacle(game_obstacle, obstacle_location)

        # Set up the enemies for first level
        enemy_list = [
            [0, 18], [10, 18], [19, 18], [1, 8], [6, 4], [15, 6]
        ]
        for enemy in enemy_list:
            x = enemy[0]
            y = enemy[1]
            game_enemy = Enemy(x, y)
            enemy_location = Coordinates(x, y)
            self.first_level.add_enemy(game_enemy, enemy_location)

        # Set up the coins for first level
        coin_list = [
            [0, 15], [11, 14], [19, 16], [9, 11], [11, 6], [5, 5], [0, 9], [1, 3], [10, 2], [16, 6]
        ]
        for coin in coin_list:
            x = coin[0]
            y = coin[1]
            game_coin = Coin(x, y)
            coin_location = Coordinates(x, y)
            self.first_level.add_coin(game_coin, coin_location)

        # Set up the goal for first level
        goal_location = Coordinates(19, 0)
        self.first_level.add_goal(goal_location)

        # Set up the second level
        self.second_level = Level(20, 20)

        # Set up the obstacles for second level
        coordinate_list = [
            [3, 15], [4, 14], [5, 14], [17, 12], [18, 11], [19, 9], [18, 7], [15, 10], [5, 10], [0, 3], [3, 3],
            [3, 2], [11, 2], [12, 3], [13, 3], [14, 3], [15, 2], [3, 15], [0, 19], [1, 19], [2, 19], [3, 19],
            [4, 19], [5, 19], [6, 19], [7, 19], [8, 19], [9, 19], [10, 19], [11, 19], [12, 19], [13, 19], [14, 19],
            [15, 19], [16, 19], [17, 19], [18, 19], [19, 19], [8, 18], [9, 18], [9, 17], [9, 18], [15, 16],
            [14, 15], [13, 14], [12, 14], [12, 13], [12, 12], [12, 11], [11, 11], [8, 11], [7, 11], [6, 11], [4, 9],
            [3, 9], [2, 9], [1, 9], [1, 6], [4, 4], [5, 4], [6, 5], [7, 5], [8, 5], [9, 5], [11, 6], [12, 7],
            [13, 7], [14, 7], [15, 7], [16, 7], [17, 7], [17, 6], [17, 5], [17, 4], [18, 3], [19, 3]
        ]
        for coordinate in coordinate_list:
            x = coordinate[0]
            y = coordinate[1]
            game_obstacle = Obstacle(x, y)
            obstacle_location = Coordinates(x, y)
            self.second_level.add_obstacle(game_obstacle, obstacle_location)

        # Set up the enemies for second level
        enemy_list = [
            [3, 18], [5, 18], [14, 14], [18, 10], [7, 10], [3, 8], [4, 3], [12, 2], [13, 2], [14, 6]
        ]
        for enemy in enemy_list:
            x = enemy[0]
            y = enemy[1]
            game_enemy = Enemy(x, y)
            enemy_location = Coordinates(x, y)
            self.second_level.add_enemy(game_enemy, enemy_location)

        # Set up the coins for second level
        coin_list = [
            [4, 15], [13, 15], [15, 9], [18, 4], [10, 6], [0, 6], [0, 0], [14, 4], [13, 0]
        ]
        for coin in coin_list:
            x = coin[0]
            y = coin[1]
            game_coin = Coin(x, y)
            coin_location = Coordinates(x, y)
            self.second_level.add_coin(game_coin, coin_location)

        # Set up the goal for second level
        goal_location = Coordinates(19, 0)
        self.second_level.add_goal(goal_location)

        # Set up the third level
        self.third_level = Level(20, 20)

        # Set up the obstacles for third level
        coordinate_list = [
            [0, 19], [1, 19], [2, 19], [3, 19], [4, 19], [5, 19], [6, 19], [7, 19], [8, 19], [9, 19], [10, 19],
            [11, 19], [12, 19], [13, 19], [14, 19], [15, 19], [16, 19], [17, 19], [18, 19], [19, 19], [5, 18],
            [6, 17], [7, 16], [8, 15], [8, 14], [8, 13], [4, 12], [0, 12], [15, 15], [14, 15], [14, 14], [13, 13],
            [11, 11], [10, 10], [9, 10], [9, 9], [8, 8], [7, 7], [4, 6], [3, 6], [2, 6], [5, 2], [9, 4], [10, 4],
            [11, 6], [12, 6], [12, 5], [12, 4], [12, 3], [12, 2], [12, 1], [12, 0], [13, 6], [14, 9], [15, 9],
            [16, 10], [17, 10], [18, 10], [19, 10], [18, 5], [17, 5], [17, 2], [16, 1]
        ]
        for coordinate in coordinate_list:
            x = coordinate[0]
            y = coordinate[1]
            game_obstacle = Obstacle(x, y)
            obstacle_location = Coordinates(x, y)
            self.third_level.add_obstacle(game_obstacle, obstacle_location)

        # Set up the enemies for third level
        enemy_list = [
            [3, 18], [4, 18], [11, 18], [14, 13], [9, 8], [3, 5], [2, 5], [10, 3], [11, 5], [15, 8], [19, 9]
        ]
        for enemy in enemy_list:
            x = enemy[0]
            y = enemy[1]
            game_enemy = Enemy(x, y)
            enemy_location = Coordinates(x, y)
            self.third_level.add_enemy(game_enemy, enemy_location)

        # Set up the coins for third level
        coin_list = [
            [0, 11], [0, 4], [8, 18], [19, 18], [5, 1], [11, 0], [13, 5], [18, 9], [16, 0]
        ]
        for coin in coin_list:
            x = coin[0]
            y = coin[1]
            game_coin = Coin(x, y)
            coin_location = Coordinates(x, y)
            self.third_level.add_coin(game_coin, coin_location)

        # Set up the goal for third level
        goal_location = Coordinates(19, 0)
        self.third_level.add_goal(goal_location)

        # Set up the fourth level...

# SETTING UP THE APPLICATION AND ALLOWING USER INTERACTION -------------------------------------------------------------


def main():
    """
    Setup the game.
    """
    # Every Qt application must have one instance of QApplication.
    global app  # Use global to prevent crashing on exit
    app = QApplication(sys.argv)
    gui = GameGUI(SQUARE_SIZE)

    # Start the Qt event loop. (i.e. make it possible to interact with the gui)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
