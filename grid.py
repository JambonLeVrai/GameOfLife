from cell import Cell
from ruleset import RuleSet
import numpy as np

class Grid:
    def __init__(self, width, height, ruleset):
        self.width = width
        self.height = height
        self.ruleset = ruleset
        self.grid = [[Cell(x=x, y=y) for x in range(width)] for y in range(height)]
        self.neighbours_list = [[self.get_neighbours(self.grid[y][x]) for x in range(width)] for y
                                 in range(height)]


    def randomise(self):
        for x in range(self.width):
            for y in range(self.height):
                n_status = int(np.log10(self.ruleset.max_status))
                #print("n_status:", n_status, "max_status: ", self.ruleset.max_status)
                self.grid[y][x].status_actual = np.random.choice([0]+[10**i for i in range(
                    n_status+1)])
                if self.grid[y][x].status_actual == self.ruleset.max_status:
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
                #neighbours = self.get_neighbours(self.grid[y][x])
                neighbours = self.neighbours_list[y][x]
                result = ruleset.apply_rules(cell=self.grid[y][x], neighbours=neighbours)

        for x in range(self.width):
            for y in range(self.height):
                self.grid[y][x].update()

    def get_numpy_array(self):
        return np.array([[(self.ruleset.max_status-self.grid[y][x].status_actual)/self.ruleset.max_status*255 for x in range(self.width)] for y in range(self.height)], dtype=np.uint8)

    def __repr__(self):
        #return "grid"
        return str([[self.grid[y][x].status_actual for x in range(self.width)] for y in range(self.height)])

if __name__ == '__main__':
    ruleset_test = RuleSet(conway=False, brian=True)
    grid_test = Grid(width=10, height=10, ruleset=ruleset_test)
    grid_test.randomise()
    print(grid_test)
    #print(ruleset_test.dict)
    for i in range(5):
        grid_test.next_turn(ruleset_test)
        print(grid_test)

    #grid_test.grid[2][2].status_actual = 1
    #grid_test.grid[2][1].status_actual = 1
    #grid_test.grid[1][2].status_actual = 1
    #for i in range(2):
    #    grid_test.next_turn(ruleset_test)
    #print(grid_test)