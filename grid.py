from cell import Cell, max_status, min_status
from ruleset import RuleSet
import numpy as np

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x=x, y=y) for x in range(width)] for y in range(height)]

    def randomize(self):
        self.grid = [[Cell(x=x, y=y, status_actual=np.random.randint(min_status, max_status+1) ) for x in range(self.width)] for y in range(self.height)]

    def get_neighbours(self, cell: Cell):
        #Par défaut: les cellules au bord de la grille sont mortes (= ne pas les mettre dans la liste)
        xi, yi = cell.x, cell.y
        Neighbours = []
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if not(dx == 0 and dy == 0):
                    if 0 <= xi+dx < self.width and 0 <= yi + dy < self.height:
                        Neighbours.append(self.grid[yi+dy][xi+dx])

        return Neighbours

    def next_turn(self):
        for x in range(grid.width):
            for y in range(grid.height):
                neighbours = grid.get_neighbours(grid.grid[y][x])
                result = ruleset.apply_rules(cell=grid.grid[y][x], neighbours=neighbours)

        for x in range(grid.width):
            for y in range(grid.height):
                self.grid[y][x].update()

    def __repr__(self):
        #return "grid"
        return str([[self.grid[y][x].status_actual for x in range(self.width)] for y in range(self.height)])

if __name__ == '__main__':
    grid = Grid(width=5, height=5)
    ruleset = RuleSet()
    grid.grid[2][2].status_actual = 1
    grid.grid[2][1].status_actual = 1
    grid.grid[1][2].status_actual = 1
    print(grid)
    grid.next_turn()
    print(grid)