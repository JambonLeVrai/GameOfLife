import numpy as np
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget


class GridImage(QWidget):
    def __init__(self):
        super().__init__()
        self.image_data = None
        self.zoom = 1

    def set_image_data(self, data: np.ndarray):
        self.image_data = data
        self.update()

    def paintEvent(self, event) -> None:
        if self.image_data is None:
            return

        height, width = self.image_data.shape
        bytes_per_line = width
        qimage = QImage(
            self.image_data.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_Grayscale8
        )

        self.set_zoom(self.zoom)

        painter = QPainter(self)
        painter.drawImage(self.rect(), qimage)

    def set_zoom(self, zoom_level):
        self.setFixedWidth(self.image_data.shape[1] * zoom_level)
        self.setFixedHeight(self.image_data.shape[0] * zoom_level)
        self.zoom = zoom_level