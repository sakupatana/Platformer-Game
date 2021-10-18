import unittest
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QTransform, QColor

from coordinates import Coordinates
from character import Character
from enemy import Enemy
from coin import Coin
from obstacle import Obstacle
from gameGUI import GameGUI
from square import Square
from enemy_graphics_item import EnemyGraphicsItem
from coin_graphics_item import CoinGraphicsItem

app = QApplication(sys.argv)


class Test(unittest.TestCase):
    """
    Some tests for the Platformer project.
    """
    def setUp(self):
        """
        This set ups the GUI.
        """
        self.game = GameGUI(30)

    def test_level_setup(self):
        """
        Test that the setup of the level works.
        """
        # Test character setup
        self.assertEqual("Test", self.game.character.get_name(), "The name of the character is wrong.")
        self.assertNotEqual(None, self.game.character.get_location(), "The location of character is not added")
        test_empty_location = Coordinates(5, 17)
        test_character = Character("Test2")
        test_character.set_level(self.game.game, test_empty_location)
        self.assertEqual(5, test_character.get_location().get_x(), "The character level has not been set successfully.")
        self.assertEqual(17, test_character.get_location().get_y(),
                         "The character level has not been set successfully.")
        self.assertEqual(self.game.game, test_character.get_level(),
                         "The character level has not been set successfully.")

        # Test level setupTest
        self.assertEqual(20, self.game.game.get_height(), "The height of the level is wrong.")
        self.assertEqual(20, self.game.game.get_width(), "The width of the level is wrong.")
        self.assertNotEqual(None, self.game.game.get_coins(), "The coins have not been added successfully.")
        self.assertNotEqual(None, self.game.game.get_enemies(), "The enemies have not been added successfully.")
        self.assertNotEqual(None, self.game.game.get_obstacles(), "The obstacles have not been added successfully.")
        self.assertEqual(57, len(self.game.game.get_obstacles()), "The obstacles have not been added successfully.")
        self.assertEqual(9, len(self.game.game.get_coins()), "The number of coins is wrong.")
        self.assertEqual(6, len(self.game.game.get_enemies()), "The number of coins is wrong.")
        self.assertNotEqual(None, self.game.game.get_character(), "The character has not been added to level")
        goal_location = Coordinates(2, 18)
        self.assertEqual(True, self.game.game.add_goal(goal_location), "The goal has not been added successfully.")
        obstacle_coordinates = Coordinates(0, 0)
        new_obstacle = Obstacle(0, 0)
        self.assertEqual(True, self.game.game.add_obstacle(new_obstacle, obstacle_coordinates),
                         "The obstacle has not been added successfully.")
        game_coin = Coin(10, 10)
        coin_location = game_coin.get_location()
        self.assertEqual(True, self.game.game.add_coin(game_coin, coin_location),
                         "The coin has not been created successfully.")
        game_enemy = Enemy(12, 0)
        enemy_location = game_enemy.get_location()
        self.assertEqual(True, self.game.game.add_enemy(game_enemy, enemy_location),
                         "The enemy has not been created successfully.")
        self.assertEqual(self.game.character, self.game.game.character, "The character of the level is wrong")
        self.assertNotEqual([], self.game.game.obstacles, "The obstacles are not added into the level")
        self.assertNotEqual([], self.game.game.enemies, "The enemies are not added into the level")
        self.assertNotEqual([], self.game.game.coins, "The coins are not added into the level")

        # Test squares setup
        self.assertEqual(False, self.game.game.get_square(coin_location).set_coin(),
                         "The coin has not been added to the square successfully.")
        self.assertEqual(False, self.game.game.get_square(enemy_location).set_enemy(),
                         "The enemy has not been added to the square successfully.")
        self.assertEqual(False, self.game.game.get_square(goal_location).set_goal(),
                         "The goal has not been added to the square successfully.")
        self.assertEqual(False, self.game.game.get_square(coin_location).set_obstacle(),
                         "The obstacle adding is not working properly")
        self.assertEqual(True, self.game.game.get_square(coin_location).is_coin_square(),
                         "The square of the coin is not added correctly")
        self.assertEqual(True, self.game.game.get_square(enemy_location).is_enemy_square(),
                         "The square of the enemy is not added correctly")
        self.assertEqual(True, self.game.game.get_square(obstacle_coordinates).is_obstacle_square(),
                         "The square of the obstacle is not added correctly")
        self.assertEqual(True, self.game.game.get_square(goal_location).is_goal_square(),
                         "The square of the goal is not added correctly")
        empty_location = Coordinates(8, 0)
        self.assertEqual(True, self.game.game.get_square(empty_location).is_empty(),
                         "The square is not empty even it should be")
        self.assertEqual(False, self.game.game.get_square(enemy_location).is_empty(),
                         "The square is empty even it should not be")
        Square.remove_coin(self.game.game.get_square(coin_location))
        self.assertEqual(False, self.game.game.get_square(coin_location).is_coin_square(),
                         "The square of the coin is not removed correctly")

        # Test enemies setup
        self.assertEqual(12, game_enemy.get_location().get_x(), "The enemy x value is wrong.")
        self.assertEqual(0, game_enemy.get_location().get_y(), "The enemy y value is wrong.")

        # Test coins setup
        self.assertEqual(10, game_coin.get_location().get_x(), "The coin x value is wrong.")
        self.assertEqual(10, game_coin.get_location().get_y(), "The coin y value is wrong.")
        self.assertEqual(1, game_coin.get_value(), "The coin value is wrong.")

        # Test coordinates setup
        self.assertEqual(2, goal_location.get_x(), "The coordinates bring wrong value for x.")
        self.assertEqual(18, goal_location.get_y(), "The coordinates bring wrong value for y.")

        # Test that all the objects are added to the current game
        self.assertEqual(self.game.character, self.game.character, "The character of the game is not correct")
        self.assertEqual(self.game.game, self.game.game, "The level of the game is not correct")
        self.assertNotEqual([], self.game.added_coin_items, "The coin items are not added into the game correctly")
        self.assertNotEqual([], self.game.added_coins, "The coins are not added into the game correctly")
        self.assertNotEqual([], self.game.added_enemies, "The enemies are not added into the game correctly")

    def test_window_setup(self):
        """
        Test the window setup that everything has been created accordingly.
        """
        # Test the scene setup
        self.assertEqual(500, self.game.scene.height(), "The scene height is wrong")
        self.assertEqual(500, self.game.scene.width(), "The scene width is wrong")
        self.assertNotEqual(None, self.game.view.show, "The scene is not created accordingly")
        self.assertNotEqual(None, self.game.scene.items())

        # Test the score text setup
        self.assertEqual(QRect(30, 200, 100, 50), self.game.score_text.geometry(), "The score text is placed wrong")

        # Test the result text setup
        self.assertEqual(QRect(325, 100, 260, 60), self.game.result.geometry(), "The result text is placed wrong")

        # Test the exit game button setup
        self.assertEqual(QRect(500, 38, 200, 50), self.game.exit_game.geometry(),
                         "The exit game button is placed wrong")
        self.assertEqual("Exit the game", self.game.exit_game.text(), "The text in the exit game button is wrong")

        # Test the reset game button setup
        self.assertEqual(QRect(200, 38, 200, 50), self.game.reset_game.geometry(),
                         "The reset game button is placed wrong")
        self.assertEqual("Restart the level", self.game.reset_game.text(), "The text in the reset game button is wrong")

        # Test the main window setup
        self.assertEqual(900, self.game.width(), "The width of the main window is wrong")
        self.assertEqual(900, self.game.height(), "The height of the main window is wrong")
        self.assertEqual(QRect(400, 100, 900, 900), self.game.geometry(), "The location of the main window is wrong")
        self.assertEqual("Platformer", self.game.windowTitle(), "The title of the main window is wrong")
        self.assertNotEqual(None, self.game.show, "The main window is not created accordingly")

    def test_graphics_items(self):
        """
        Test the graphics items of every object: enemy, character, coin, grid.
        """
        # Test the character graphics item
        self.assertNotEqual(None, self.game.character_graphics_item, "The character item is not added successfully")
        self.assertEqual(self.game.character_graphics_item, self.game.character.graphics_item,
                         "An incorrect character item is added")
        self.assertEqual(QPointF((1 * self.game.square_size), (18 * self.game.square_size)),
                         self.game.character_graphics_item.scenePos(),
                         "The character item is not added to the scene correctly")

        # Test the enemy graphics item
        red = QColor(255, 0, 0)
        game_enemy = Enemy(12, 0)
        enemy_item = EnemyGraphicsItem(game_enemy, self.game.square_size, red)
        self.assertEqual(QPointF((12 * self.game.square_size), (0 * self.game.square_size)),
                         enemy_item.scenePos(), "The enemy item is not added to the scene correctly")

        # Test the coin graphics item
        yellow = QColor(255, 255, 0)
        game_coin = Coin(10, 10)
        coin_item = CoinGraphicsItem(game_coin, self.game.square_size, yellow)
        self.assertEqual(QPointF((10 * self.game.square_size), (10 * self.game.square_size)),
                         coin_item.scenePos(), "The coin item is not added to the scene correctly")

        # Test the grid graphics item
        self.assertNotEqual(None, self.game.scene.itemAt(1, 15, QTransform()),
                            "The grid item is not added to the scene correctly")

    def test_moving(self):
        """
        Test moving processes.
        """
        # Moving right
        self.game.character.try_move(10, 10)
        window = self.game.widget
        QTest.keyEvent(QTest.Press, window, Qt.Key_D)
        self.assertEqual(11, self.game.character.get_location().get_x(),
                         "The character is not moved to right correctly")

        # Moving left
        QTest.keyEvent(QTest.Press, window, Qt.Key_A)
        self.assertEqual(10, self.game.character.get_location().get_x(), "The character is not moved to left correctly")

        # Moving down
        QTest.keyEvent(QTest.Press, window, Qt.Key_S)
        self.assertEqual(11, self.game.character.get_location().get_y(), "The character is not moved to down correctly")

        # Moving up
        QTest.keyEvent(QTest.Press, window, Qt.Key_W)
        self.assertEqual(10, self.game.character.get_location().get_x(), "The character is not moved to up correctly")

        # Incorrect event and no moving
        QTest.keyEvent(QTest.Press, window, Qt.Key_G)
        self.assertEqual(10, self.game.character.get_location().get_x(), "The character is moving with incorrect event")
        self.assertEqual(11, self.game.character.get_location().get_y(), "The character is moving with incorrect event")

    def test_collisions(self):
        """
        Test the collision detection to objects: enemy, coin, goal, obstacle.
        """
        # Obstacle collision
        window = self.game.widget
        self.assertNotEqual(True, self.game.character.try_move(0, 19), "The collision with obstacle is not detected")

        # Coin collision
        self.game.character.try_move(0, 15)
        self.assertEqual(True, self.game.check_coin_collision(), "The collision with coin is not detected")

        # Enemy collision
        self.game.character.try_move(1, 18)
        QTest.keyEvent(QTest.Press, window, Qt.Key_A)
        self.assertEqual(True, self.game.check_enemy_collision(), "The collision with enemy is not detected")

        # Goal collision
        self.game.character.try_move(18, 0)
        self.game.stopped = False
        QTest.keyEvent(QTest.Press, window, Qt.Key_D)
        self.assertEqual(True, self.game.check_goal_collision(), "The collision with goal is not detected")

    def test_losing(self):
        """
        Test the losing process.
        """
        game_enemy2 = Enemy(0, 18)
        enemy_location2 = Coordinates(0, 18)
        self.game.character.try_move(1, 18)
        self.game.game.add_enemy(game_enemy2, enemy_location2)
        window = self.game.widget
        QTest.keyEvent(QTest.Press, window, Qt.Key_A)
        self.assertEqual("You have lost", self.game.result.text(), "The losing text is not working correctly")
        self.assertEqual(True, self.game.stopped, "The game is not stopped when player lose the game")

    def test_winning(self):
        """
        Test the winning process.
        """
        window = self.game.widget
        self.game.character.try_move(18, 0)
        QTest.keyEvent(QTest.Press, window, Qt.Key_D)
        self.assertEqual("You have won", self.game.result.text(), "The winning text is not working correctly")
        self.assertEqual(True, self.game.stopped, "The game is not stopped when player win the game")
        self.assertEqual(True, self.game.next_level.isVisible(), "The next level button is not visible after winning")

    def test_collecting_points(self):
        """
        Test points (coins) collection.
        """
        new_location = Coordinates(0, 15)
        self.game.character.try_move(1, 15)
        window = self.game.widget
        QTest.keyEvent(QTest.Press, window, Qt.Key_A)
        self.assertEqual(1, self.game.score, "The score is not working correctly")
        self.assertEqual(False, self.game.game.get_square(new_location).is_coin_square(),
                         "The square is not set to empty after collecting a coin")
        self.assertEqual(8, len(self.game.added_coins),
                         "The number of coins is not decreased after collecting a coin")

    def test_jumping(self):
        """
        Test the jumping.
        """
        # Jumping without an obstacle above
        window = self.game.widget
        QTest.keyEvent(QTest.Press, window, Qt.Key_W)
        self.assertEqual(True, self.game.jump, "The jumping is not activated correctly")
        self.game.jumping()
        self.assertEqual(1, self.game.jump_height, "The jumping is not working correctly")

        # Jumping under an obstacle
        self.game.character.try_move(11, 12)
        QTest.keyEvent(QTest.Press, window, Qt.Key_W)
        self.game.jumping()
        self.assertEqual(0, self.game.jump_height, "The jumping is not detecting obstacle correctly")
        self.assertEqual(False, self.game.jump, "The jumping is not stopped after detecting an obstacle")
        self.assertEqual(True, self.game.gravity, "The gravity is not activated after detecting an obstacle")

    def test_gravitation(self):
        """
        Test the gravitation.
        """
        # Gravity without an obstacle below
        self.game.character.try_move(1, 10)
        window = self.game.widget
        QTest.keyEvent(QTest.Press, window, Qt.Key_S)
        self.assertEqual(True, self.game.gravity, "The gravity is not activated correctly")
        self.game.gravity_activate()
        self.assertEqual(12, self.game.character.get_location().get_y(), "The gravity is not activated correctly")

        # Gravity above an obstacle
        self.game.character.try_move(11, 10)
        self.game.gravity_activate()
        self.assertEqual(False, self.game.gravity, "The gravity is activated although should not be")

    def test_create_level(self):
        """
        Test the process of creating levels.
        """
        # Test creating second level
        self.game.game = self.game.second_level
        # Check enemy location in second level
        enemy_location = Coordinates(3, 18)
        self.assertEqual(True, self.game.game.get_square(enemy_location).is_enemy_square(),
                         "The enemy is not added to next level")
        # Check coin location in second level
        coin_location = Coordinates(10, 6)
        self.assertEqual(True, self.game.game.get_square(coin_location).is_coin_square(),
                         "The coin is not added to next level")
        # Check goal location in second level
        goal_location = Coordinates(19, 0)
        self.assertEqual(True, self.game.game.get_square(goal_location).is_goal_square(),
                         "The goal is not added to next level")

        # Test creating third level
        self.game.game = self.game.third_level
        # Check enemy location in second level
        enemy_location = Coordinates(9, 8)
        self.assertEqual(True, self.game.game.get_square(enemy_location).is_enemy_square(),
                         "The enemy is not added to next level")
        # Check coin location in second level
        coin_location = Coordinates(5, 1)
        self.assertEqual(True, self.game.game.get_square(coin_location).is_coin_square(),
                         "The coin is not added to next level")
        # Check goal location in second level
        goal_location = Coordinates(19, 0)
        self.assertEqual(True, self.game.game.get_square(goal_location).is_goal_square(),
                         "The goal is not added to next level")

    def test_handling_results(self):
        """
        Test loading the results from text file.
        """
        self.game.load_results()
        self.assertNotEqual(None, self.game.results, "The results are not loaded correctly")
        self.assertNotEqual(0, len(self.game.results), "The results file is empty although it should not be")
        self.assertNotEqual(0, len(self.game.top_scores.text()), "The top scores are not filled correctly")

    def test_buttons_labels(self):
        """
        Test the buttons and labels in the GUI.
        """
        # Game reset button functionality
        reset_button = self.game.reset_game
        QTest.mouseClick(reset_button, Qt.LeftButton)
        self.assertEqual(False, self.game.stopped, "The game is stopped after resetting")
        self.assertEqual(1, self.game.character.get_location().get_x(),
                         "The reset button doesn't relocate the character correctly")
        self.assertEqual(18, self.game.character.get_location().get_y(),
                         "The reset button doesn't relocate the character correctly")
        self.assertEqual("", self.game.result.text(), "The result label is not emptied correctly")
        self.assertEqual(0, self.game.score, "The score of the game is not reset to zero")
        coin_location = Coordinates(0, 15)
        self.assertEqual(0, coin_location.get_x(), "The x location of coin is not reset correctly")
        self.assertEqual(15, coin_location.get_y(), "The y location of coin is not reset correctly")
        self.assertEqual(True, self.game.game.get_square(coin_location).is_coin_square(),
                         "The square of the coin is not reset correctly ")

        # Next level button functionality
        next_level_button = self.game.next_level
        QTest.mouseClick(next_level_button, Qt.LeftButton)
        self.assertEqual(2, self.game.level, "The level is not changed accordingly")
        self.assertEqual(self.game.game, self.game.second_level, "New level is not created")

        self.assertEqual(False, self.game.stopped, "The game is still stopped after pressing next level")
        self.assertEqual(0, self.game.score, "The score of the game is not reset to zero")
        self.assertEqual(False, self.game.next_level.isVisible(), "The next button is still visible after pressing")
        self.assertEqual(True, self.game.previous_level.isVisible(), "The previous button is not visible")
        self.assertEqual("", self.game.result.text(), "The result label is not emptied correctly")
        self.assertEqual(1, self.game.character.get_location().get_x(),
                         "The next level button doesn't relocate the character correctly")
        self.assertEqual(18, self.game.character.get_location().get_y(),
                         "The next level button doesn't relocate the character correctly")

        # Previous level button functionality
        previous_level_button = self.game.previous_level
        QTest.mouseClick(previous_level_button, Qt.LeftButton)
        self.assertEqual(1, self.game.level, "The level is not changed accordingly")
        self.assertEqual(self.game.game, self.game.first_level, "New level is not created")
        self.assertEqual(False, self.game.stopped, "The game is still stopped after pressing next level")
        self.assertEqual(0, self.game.score, "The score of the game is not reset to zero")
        self.assertEqual(True, self.game.next_level.isVisible(), "The next button is still visible after pressing")
        self.assertEqual(False, self.game.previous_level.isVisible(), "The previous button is not visible")
        self.assertEqual("", self.game.result.text(), "The result label is not emptied correctly")
        self.assertEqual(1, self.game.character.get_location().get_x(),
                         "The next level button doesn't relocate the character correctly")
        self.assertEqual(18, self.game.character.get_location().get_y(),
                         "The next level button doesn't relocate the character correctly")
        # Test again the next level button
        self.game.lv2_finished = True
        QTest.mouseClick(next_level_button, Qt.LeftButton)
        self.assertEqual(True, self.game.next_level.isVisible(), "The next button is not visible")
        self.assertEqual(True, self.game.previous_level.isVisible(), "The previous button is not visible")

        # Game result text label functionality
        self.assertEqual("", self.game.result.text(), "The result label has wrong value in the beginning")
        game_over_lose = -1
        self.game.check_result(game_over_lose)
        self.assertEqual("You have lost", self.game.result.text(), "The result label has wrong text after losing")
        game_over_win = 1
        self.game.check_result(game_over_win)
        self.assertEqual("You have won", self.game.result.text(), "The result label has wrong text after winning")
        self.game.reset_level()
        self.assertEqual("", self.game.result.text(), "The result label has wrong text after resetting the game")

        # The end result label functionality
        self.assertEqual(False, self.game.end_result.isVisible(), "The end result label is visible in the beginning")
        self.game.level = 3
        self.game.check_result(game_over_win)
        self.assertEqual(True, self.game.end_result.isVisible(),
                         "The end result label is not visible after completing the game")
        self.assertEqual("Congratulations! You have successfully passed all the levels of the game",
                         self.game.end_result.text(), "The end result label is not visible after completing the game")


if __name__ == "__main__":
    unittest.main()
