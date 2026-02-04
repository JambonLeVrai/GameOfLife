from cell import Cell, max_status, min_status
from ruleset import RuleSet
import numpy as np

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x=x, y=y) for x in range(width)] for y in range(height)]

    def randomise(self):
        self.grid = [[Cell(x=x, y=y, status_actual=np.random.randint(min_status, max_status+1) ) for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x].status_actual == max_status:
                    self.grid[y][x].color = 0

    def get_neighbours(self, cell: Cell):
        #Par défaut: les cellules au bord de la grille sont mortes (= ne pas les mettre dans la liste)
        xi, yi = cell.x, cell.y
        Neighbours = [
            self.grid[yi + dy][xi + dx]
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if not (dx == 0 and dy == 0)
            if 0 <= xi + dx < self.width and 0 <= yi + dy < self.height
        ]
        return Neighbours

    def next_turn(self, ruleset):
        for x in range(self.width):
            for y in range(self.height):
                neighbours = self.get_neighbours(self.grid[y][x])
                result = ruleset.apply_rules(cell=self.grid[y][x], neighbours=neighbours)

        for x in range(self.width):
            for y in range(self.height):
                self.grid[y][x].update()
                if self.grid[y][x].status_actual == max_status:
                    self.grid[y][x].color = 0

    def __repr__(self):
        #return "grid"
        return str([[self.grid[y][x].status_actual for x in range(self.width)] for y in range(self.height)])

if __name__ == '__main__':
    grid_test = Grid(width=5, height=5)
    ruleset_test = RuleSet()
    grid_test.grid[2][2].status_actual = 1
    grid_test.grid[2][1].status_actual = 1
    grid_test.grid[1][2].status_actual = 1
    print(grid_test)
    grid_test.next_turn(ruleset_test)
    print(grid_test)