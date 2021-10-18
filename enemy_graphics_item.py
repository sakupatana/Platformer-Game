from PyQt5 import QtWidgets, QtGui, QtCore

from coordinates import Coordinates


class EnemyGraphicsItem(QtWidgets.QGraphicsPolygonItem):
    """
    The class EnemyGraphicsItem extends QGraphicsPolygonItem to link it together to the physical
    representation of a enemy. The QGraphicsPolygonItem handles the drawing, while the enemy knows its own location.
    """
    def __init__(self, enemy, square_size, color):
        # Call init of the parent object
        super(EnemyGraphicsItem, self).__init__()

        # Do other stuff
        self.enemy = enemy
        self.square_size = square_size
        brush = QtGui.QBrush(1)  # 1 for even fill
        self.setBrush(brush)
        self.construct_triangle()
        self.setBrush(QtGui.QBrush(color))

        # Update the position of the graphics item
        self.update_position()

    def construct_triangle(self):
        """
        This method sets the shape of a enemy item into a triangle.
        """
        # Create a new QPolygon object
        triangle_enemy = QtGui.QPolygonF()

        # Add the corners of a triangle to the the polygon object
        triangle_enemy.append(QtCore.QPointF(self.square_size / 2, 0))  # Tip
        triangle_enemy.append(QtCore.QPointF(0, self.square_size))  # Bottom-left
        triangle_enemy.append(QtCore.QPointF(self.square_size, self.square_size))  # Bottom-right
        triangle_enemy.append(QtCore.QPointF(self.square_size / 2, 0))  # Tip

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle_enemy)

        # Set the origin of transformations to the center of the square.
        self.setTransformOriginPoint(self.square_size/2, self.square_size/2)

    def update_position(self):
        """
        This method updates the position of a enemy's graphic item.
        """
        location = self.enemy.get_location()
        x = Coordinates.get_x(location)
        y = Coordinates.get_y(location)
        self.setPos((self.square_size * x), (self.square_size * y))

    def get_enemy(self):
        """
        This method returns the enemy object of this enemy graphic item.
        """
        return self.enemy
