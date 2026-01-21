from cell import Cell, max_status, min_status
import numpy as np

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x=x, y=y) for x in range(width)] for y in range(height)]

    def next_turn(self):
        pass

    def get_neighbors(self, cell: Cell):
        pass

    def randomize(self):
        self.grid = [[Cell(x=x, y=y, status_actual=np.random.randint(min_status, max_status+1) ) for x in range(self.width)] for y in range(self.height)]

if __name__ == '__main__':
    grid = Grid(width=5, height=5)
