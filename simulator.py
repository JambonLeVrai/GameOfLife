import numpy as np


class Simulator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buffer = np.zeros((self.width, self.height), dtype=np.uint8)

    def simulate(self):
        # self.buffer = np.astype(np.trunc(np.random.rand(self.height, self.width) * 255), np.uint8)
        self.buffer += np.ones_like(self.buffer)

    def get_data_copy(self):
        return np.copy(self.buffer)