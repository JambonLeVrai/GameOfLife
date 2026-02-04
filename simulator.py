import numpy as np

from grid import Grid
from ruleset import RuleSet


class Simulator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buffer = np.zeros((self.width, self.height), dtype=np.uint8)

        self.grid = Grid(width=self.width, height=self.height)
        self.rule_set = RuleSet()
        #self.grid.grid[2][2].status_actual = 1
        #self.grid.grid[2][1].status_actual = 1
        #self.grid.grid[2][3].status_actual = 1
        self.grid.randomise()

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buffer = np.zeros((self.width, self.height), dtype=np.uint8)
        self.grid = Grid(width=self.width, height=self.height)
        self.grid.randomise()

    def simulate(self):
        # self.buffer = np.astype(np.trunc(np.random.rand(self.height, self.width) * 255), np.uint8)
        # self.buffer += np.ones_like(self.buffer)
        self.grid.next_turn(self.rule_set)
        self.buffer = self.grid.get_numpy_array()

    def get_data_copy(self):
        return np.copy(self.buffer)