from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QSpinBox, QLabel, QComboBox
from PyQt6.QtGui import QImage, QPainter, QPixmap
import numpy as np
import sys


class MainWidget(QWidget):
    def __init(self, parent=None):
        super().__init__(parent)
        self.my_layout = QVBoxLayout()

        self.my_button = QPushButton('Test')
        self.my_layout.addWidget(self.my_button)

        self.setLayout(self.my_layout)


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Top row
        self.top_row = QWidget()
        top_row_layout = QHBoxLayout()
        zoom_level_label = QLabel('Zoom level')
        top_row_layout.addWidget(zoom_level_label, 0)

        self.zoom_level = QComboBox()
        self.zoom_level.addItems(['1', '2', '3', '4', '5'])
        top_row_layout.addWidget(self.zoom_level, 1)
        layout.addLayout(top_row_layout)

        self.zoom_level.currentIndexChanged.connect(self.update_zoom_level)

        self.grid_image = GridImage()
        layout.addWidget(self.grid_image)

        # Play
        play_row_layout = QHBoxLayout()
        self.play_pause = QPushButton('Play')
        self.status = 'paused'
        self.play_pause.clicked.connect(self.play_pause_clicked)
        play_row_layout.addWidget(self.play_pause, 1)

        self.step = QSpinBox()
        self.step.setReadOnly(True)
        self.step.setValue(0)
        play_row_layout.addWidget(self.step, 0)

        layout.addLayout(play_row_layout)

        # Speed
        speed_label = QLabel('Target speed (steps/s)')
        self.speed_spin = QSpinBox()
        self.speed_spin.setMinimum(1)
        speed_row_layout = QHBoxLayout()
        speed_row_layout.addWidget(speed_label, 0)
        speed_row_layout.addWidget(self.speed_spin, 1)
        layout.addLayout(speed_row_layout)

        # Grid dimensions
        grid_dimension_label = QLabel('Grid dimensions')
        self.width_spin = QSpinBox()
        self.width_spin.setMinimum(1)
        self.width_spin.setMaximum(2000)
        self.width_spin.setValue(255)
        self.height_spin = QSpinBox()
        self.height_spin.setMinimum(1)
        self.height_spin.setMaximum(2000)
        self.height_spin.setValue(255)
        self.apply_grid_dimensions_w = QPushButton('Apply')
        self.apply_grid_dimensions_w.clicked.connect(self.apply_grid_dimensions)
        grid_dimension_layout = QHBoxLayout()
        grid_dimension_layout.addWidget(grid_dimension_label)
        grid_dimension_layout.addWidget(self.width_spin)
        grid_dimension_layout.addWidget(self.height_spin)
        grid_dimension_layout.addWidget(self.apply_grid_dimensions_w)
        layout.addLayout(grid_dimension_layout)

        # Reset grid
        reset_grid_layout = QHBoxLayout()
        self.clear_grid_w = QPushButton('Clear grid')
        self.clear_grid_w.clicked.connect(self.clear_grid)
        self.random_grid_w = QPushButton('Random grid')
        self.random_grid_w.clicked.connect(self.random_grid)
        reset_grid_layout.addWidget(self.clear_grid_w)
        reset_grid_layout.addWidget(self.random_grid_w)
        layout.addLayout(reset_grid_layout)

        # Rulesets
        rulesets_layout = QHBoxLayout()
        rulesets_label = QLabel('Ruleset')
        rulesets_layout.addWidget(rulesets_label, 0)
        self.rulesets_w = QComboBox()
        self.rulesets_w.addItems(['Conway'])
        self.rulesets_w.currentIndexChanged.connect(self.rulesets_changed)
        rulesets_layout.addWidget(self.rulesets_w, 1)
        layout.addLayout(rulesets_layout)

        self.disabled_list_on_play = [self.apply_grid_dimensions_w, self.clear_grid_w, self.random_grid_w]


    def update_zoom_level(self):
        zoom_level_int = int(self.zoom_level.currentText())
        self.grid_image.set_zoom(zoom_level_int)

    def play_pause_clicked(self):
        if self.status == 'paused':
            self.status = 'playing'
            self.play_pause.setText('Pause')
            self.run_simulation()
        else:
            self.status = 'paused'
            self.play_pause.setText('Play')
            self.stop_simulation()

    def run_simulation(self):
        for w in self.disabled_list_on_play:
            w.setEnabled(False)

    def stop_simulation(self):
        for w in self.disabled_list_on_play:
            w.setEnabled(True)

    def apply_grid_dimensions(self):
        # PLACEHOLDER
        my_data = np.astype(np.trunc(np.random.rand(self.height_spin.value(), self.width_spin.value()) * 255), np.uint8)
        self.grid_image.set_image_data(my_data)

    def clear_grid(self):
        # PLACEHOLDER
        my_data = np.zeros((self.height_spin.value(), self.width_spin.value()), dtype=np.uint8)
        self.grid_image.set_image_data(my_data)

    def random_grid(self):
        # PLACEHOLDER
        my_data = np.astype(np.trunc(np.random.rand(self.height_spin.value(), self.width_spin.value()) * 255), np.uint8)
        self.grid_image.set_image_data(my_data)

    def rulesets_changed(self):
        pass  # PLACEHOLDER


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    my_data = np.astype(np.trunc(np.random.rand(255, 255) * 255), np.uint8)
    window.grid_image.set_image_data(my_data)

    app.exec()

