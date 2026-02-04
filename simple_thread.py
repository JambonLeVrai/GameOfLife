import time

from PyQt6.QtCore import QMutex, QWaitCondition, QThread


class SimpleSimulationThread(QThread):

    def __init__(self, sim_obj, grid_image, step_time_ms):
        super().__init__()
        self.running = True
        self.step_time_ns = step_time_ms*1e6

        self.sim_obj = sim_obj
        self.grid_image = grid_image

        self.current_time = time.time_ns()

    def run(self):
        while self.running:
            self.compute_frame()
            self.grid_image.set_image_data(self.sim_obj.get_data_copy())

            cur_time = time.time_ns()
            if cur_time - self.current_time < self.step_time_ns:
                time.sleep((self.step_time_ns - (cur_time - self.current_time))/1e9)

            self.current_time = time.time_ns()

    def compute_frame(self):
        self.sim_obj.simulate()

    def stop(self):
        self.running = False