import time
import numpy as np

from PyQt6.QtCore import QMutex, QWaitCondition, QThread, pyqtSignal, QTimer


class SharedBuffer:
    def __init__(self):
        self.buffer = None
        self.mutex = QMutex()
        self.frame_mutex = QMutex()
        self.condition = QWaitCondition()
        self.frame_requested_flag = False
        self.frame_ready = False


class SimulationThread(QThread):

    def __init__(self, shared_buffer: SharedBuffer, sim_obj, step_time):
        super().__init__()
        self.shared_buffer = shared_buffer
        self.running = True
        self.step_time = step_time

        self.sim_obj = sim_obj

    def run(self):
        while self.running:
            self.shared_buffer.mutex.lock()
            if self.shared_buffer.frame_requested_flag:
                self.shared_buffer.frame_requested_flag = False
                self.shared_buffer.buffer = self.sim_obj.get_data_copy()
                self.shared_buffer.frame_ready = True
                self.shared_buffer.condition.wakeAll()
            self.shared_buffer.mutex.unlock()

            self.compute_frame()
            time.sleep(self.step_time)

    def compute_frame(self):
        self.sim_obj.simulate()

    def stop(self):
        self.running = False


class DisplayThread(QThread):
    def __init__(self, shared_buffer, simulation_thread, grid_image, frame_duration_ms = 30.):
        super().__init__()
        self.shared_buffer = shared_buffer
        self.simulation_thread = simulation_thread
        self.running = True
        self.frame_duration = frame_duration_ms/1000
        self.grid_image = grid_image

    def run(self):
        while self.running:
            self.request_frame()
            time.sleep(self.frame_duration)

    def request_frame(self):
        self.shared_buffer.mutex.lock()
        self.shared_buffer.frame_requested_flag = True
        self.shared_buffer.mutex.unlock()

        while not self.shared_buffer.frame_ready and self.running:
            self.shared_buffer.condition.wait(self.shared_buffer.frame_mutex)

        self.grid_image.set_image_data(self.shared_buffer.buffer)
        self.shared_buffer.frame_ready = False


    def stop(self):
        self.running = False
