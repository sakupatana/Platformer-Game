from PyQt5 import QtWidgets, QtGui, QtCore

from coordinates import Coordinates


class ObstacleGraphicsItem(QtWidgets.QGraphicsPolygonItem):
    """
    The class ObstacleGraphicsItem extends QGraphicsPolygonItem to link it together to the physical
    representation of an obstacle. The QGraphicsPolygonItem handles the drawing, while the
    obstacle knows its own location.
    """
    def __init__(self, obstacle, square_size, color):
        # Call init of the parent object
        super(ObstacleGraphicsItem, self).__init__()

        # Do other stuff
        self.obstacle = obstacle
        self.square_size = square_size
        brush = QtGui.QBrush(1)  # 1 for even fill
        self.setBrush(brush)
        self.construct_square()
        self.setBrush(QtGui.QBrush(color))

        # Update the position of the graphics item
        self.update_position()

    def construct_square(self):
        """
        This method sets the shape of character into a square.
        """
        # Create a new QPolygon object
        square_obstacle = QtGui.QPolygonF()

        # Add the corners of a square to the the polygon object
        square_obstacle.append(QtCore.QPointF(0, self.square_size))  # Bottom-left
        square_obstacle.append(QtCore.QPointF(0, 0))  # Top-left
        square_obstacle.append(QtCore.QPointF(self.square_size, 0))  # Top-right
        square_obstacle.append(QtCore.QPointF(self.square_size, self.square_size))  # Bottom-right

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(square_obstacle)

        # Set the origin of transformations to the center of the square.
        self.setTransformOriginPoint(self.square_size/2, self.square_size/2)

    def update_position(self):
        """
        Updates the position of the obstacle graphics item in the level.
        """
        location = self.obstacle.get_location()
        x = Coordinates.get_x(location)
        y = Coordinates.get_y(location)
        self.setPos((self.square_size * x), (self.square_size * y))

    def get_obstacle(self):
        """
        This method returns the obstacle object of this obstacle graphic item.
        """
        return self.obstacle
