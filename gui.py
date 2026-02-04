from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QSpinBox, QLabel, QComboBox
import numpy as np
import sys

from grid_image import GridImage
from simple_thread import SimpleSimulationThread
from simulator import Simulator
from ff_threads import FFSharedBuffer, FFDisplayThread, FFSimulationThread


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

        self.sim_obj = Simulator(255, 255)
        #self.ff_shared_buffer = FFSharedBuffer()
        #self.ff_simulation_thread = FFSimulationThread(self.ff_shared_buffer, self.sim_obj, 1e-3)
        #self.ff_display_thread = FFDisplayThread(self.ff_shared_buffer, self.ff_simulation_thread, self.grid_image)

        self.simple_simulation_thread = SimpleSimulationThread(self.sim_obj, self.grid_image, 16.67)


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

        #self.ff_simulation_thread.start()
        #self.ff_display_thread.start()
        self.simple_simulation_thread = SimpleSimulationThread(self.sim_obj, self.grid_image, 16.67)
        self.simple_simulation_thread.start()

    def stop_simulation(self):
        for w in self.disabled_list_on_play:
            w.setEnabled(True)

        #self.ff_simulation_thread.stop()
        #self.ff_display_thread.stop()
        self.simple_simulation_thread.stop()

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

