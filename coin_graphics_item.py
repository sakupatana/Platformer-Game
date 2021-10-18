from PyQt5 import QtWidgets, QtGui, QtCore

from coordinates import Coordinates


class CoinGraphicsItem(QtWidgets.QGraphicsEllipseItem):
    """
    The class CoinGraphicsItem extends QGraphicsEllipseItem to link it together to the physical
    representation of a coin. The QGraphicsEllipseItem handles the drawing, while the coin knows its own location.
    """
    def __init__(self, coin, square_size, color):
        # Call init of the parent object
        super(CoinGraphicsItem, self).__init__()

        # Do other stuff
        self.coin = coin
        self.square_size = square_size
        brush = QtGui.QBrush(1)  # 1 for even fill
        self.setBrush(brush)
        self.construct_circle()
        self.setBrush(QtGui.QBrush(color))

        # Update the position of the graphics item
        self.update_position()

    def construct_circle(self):
        """
        This method sets the shape of a coin item into a circle.
        """
        # Create a new QPolygon object
        circle_coin = QtCore.QRectF(0, 0, self.square_size, self.square_size)

        # Set this newly created ellipse as this Item's ellipse.
        self.setRect(circle_coin)

        # Set the origin of transformations to the center of the square.
        self.setTransformOriginPoint(self.square_size/2, self.square_size/2)

    def update_position(self):
        """
        This method updates the position of a coin's graphic item.
        """
        location = self.coin.get_location()
        x = Coordinates.get_x(location)
        y = Coordinates.get_y(location)
        self.setPos((self.square_size * x), (self.square_size * y))

    def get_coin(self):
        """
        This method returns the coin object of this coin graphic item.
        """
        return self.coin
