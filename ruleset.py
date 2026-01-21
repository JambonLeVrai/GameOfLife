from cell import Cell
#from grid import Grid
from typing import Callable

class RuleSet(list):
    def __init__(self, conway=True):
        #if conway is true: creating conway ruleset
        if conway:
            self.make_conway_rules()

    def create_rule(self, condition: Callable, action: Callable):
        rule = Rule(condition, action)
        self.append(rule)

    def apply_rules(self, cell: Cell, neighbours: list):
        # Caution: no overlap between the rules - maximum 1 rule should apply for each cell
        for rule in self:
            if rule.does_apply(cell, neighbours):
                rule.apply_rule(cell)
                return 0
        cell.status_next = cell.status_actual
        return 1 #nothing changes

    def make_conway_rules(self):
        def underpopulation(cell: Cell, neighbours: list):
            sum_neighbours = sum([neighbour.status_actual for neighbour in neighbours])
            actual_status = cell.status_actual
            if actual_status == 1 and sum_neighbours < 2:
                return True
            return False

        def overpopulation(cell: Cell, neighbours: list):
            sum_neighbours = sum([neighbour.status_actual for neighbour in neighbours])
            actual_status = cell.status_actual
            if actual_status == 1 and sum_neighbours > 3:
                return True
            return False

        def stay_alive(cell: Cell, neighbours: list):
            sum_neighbours = sum([neighbour.status_actual for neighbour in neighbours])
            actual_status = cell.status_actual
            if actual_status == 1 and sum_neighbours in [2,3]:
                return True
            return False

        def reproduction(cell: Cell, neighbours: list):
            sum_neighbours = sum([neighbour.status_actual for neighbour in neighbours])
            actual_status = cell.status_actual
            if actual_status == 0 and sum_neighbours == 3:
                return True
            return False

        def make_alive(cell: Cell):
            cell.status_next = 1
        def make_dead(cell: Cell):
            cell.status_next = 0

        self.create_rule(underpopulation, make_dead)
        self.create_rule(overpopulation, make_dead)
        self.create_rule(stay_alive, make_alive)
        self.create_rule(reproduction, make_alive)

class Rule:
    def __init__(self, condition: Callable[[Cell, list], bool], action: Callable[[Cell], None]):
        #Args: condition (callable): function that takes (cell, neighbours) and returns bool
        self.condition = condition
        self.action = action

    def does_apply(self, cell:Cell, neighbours: list):
        return self.condition(cell, neighbours)

    def apply_rule(self, cell: Cell):
        self.action(cell)

if __name__ == '__main__':
    from grid import Grid
    grid = Grid(width=5, height=5)
    grid.grid[2][2].status_actual = 1
    grid.grid[2][1].status_actual = 1
    grid.grid[1][2].status_actual = 1
    print(grid)
    ruleset = RuleSet(conway=True)
    for x in range(grid.width):
        for y in range(grid.height):
            neighbours = grid.get_neighbours(grid.grid[y][x])
            result = ruleset.apply_rules(cell=grid.grid[y][x], neighbours=neighbours)
    print(([[grid.grid[y][x].status_next for x in range(grid.width)] for y in range(grid.height)])
)