import numpy as np
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QPushButton
from typing import *


class GridImageContainer(QWidget):
    def __init__(self, grid_image: "GridImage"):
        super().__init__()
        layout = QHBoxLayout()
        layout.addWidget(QFrame(), stretch=1)
        layout.addWidget(grid_image)
        layout.addWidget(QFrame(), stretch=1)
        self.setLayout(layout)


class GridImage(QWidget):
    """
    Custom widget for displaying the state of the grid as a QImage
    """
    def __init__(self):
        super().__init__()
        self.image_data = None
        self.zoom = 1

    def sizeHint(self):
        """
        Reimplementation of sizeHint() to ensure that the space used by the widget
        corresponds to the expected size of the displayed QImage
        """
        if self.image_data is not None:
            return QSize(*self.image_data.shape)
        else:
            return QSize(255, 255)

    def set_image_data(self, data: np.ndarray):
        self.image_data = data
        self.update()

    def paintEvent(self, event) -> None:
        """
        Reimplementation of the paintEvent to draw the buffer data
        :param event: Default unused Qt event
        """
        if self.image_data is None:
            return

        # Generating the QImage to be rendered from the image_data buffer
        height, width = self.image_data.shape
        bytes_per_line = width*4
        qimage = QImage(
            self.image_data.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB32
        )

        # Update widget size in case something changed
        self.set_zoom(self.zoom)

        painter = QPainter(self)
        painter.drawImage(self.rect(), qimage)  # Painting the image

    def set_zoom(self, zoom_level: int):
        # Update the widget size to ensure space is properly allocated
        self.setFixedWidth(self.image_data.shape[1] * zoom_level)
        self.setFixedHeight(self.image_data.shape[0] * zoom_level)

        self.zoom = zoom_level