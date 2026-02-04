from cell import Cell
#from grid import Grid
from typing import *

class RuleSet(list):
    def __init__(self, sim_style: Literal['conway', 'brian']='conway', min_status=0, max_status=1):
        #if conway is true: creating conway ruleset
        super().__init__()
        self.min_status = min_status
        self.max_status = max_status
        match sim_style:
            case 'conway':
                self.make_conway_rules()
            case 'brian':
                self.make_brian_rules()

        self.dict = {}
        for status in range(min_status, self.max_status+1):
            for sum_neighbours in range(8*min_status, 8*self.max_status+1):
                rule_found = False
                for rule in self:
                    if rule.does_apply(status, sum_neighbours):
                        self.dict[(status, sum_neighbours)] = rule.apply_rule
                        rule_found = True
                        break
                if not rule_found:
                    self.dict[(status, sum_neighbours)] = self.no_rule_applies


    def no_rule_applies(self, cell: Cell):
        cell.status_next = cell.status_actual

    def create_rule(self, condition: Callable, action: Callable):
        rule = Rule(condition, action)
        self.append(rule)

    def apply_rules(self, cell: Cell, neighbours: list):
        # Caution: no overlap between the rules - maximum 1 rule should apply for each cell
        sum_neighbours = sum([neighbour.status_actual for neighbour in neighbours])
        status = cell.status_actual
        self.dict[(status, sum_neighbours)](cell)


    def make_brian_rules(self):
        self.max_status = 10
        def is_dying(status, sum_neighbours: int):
            #Cells that were in the dying state go into the off state
            if status==1:
                return True
            return False
        def is_alive(status, sum_neighbours: int):
            #All cells that were "on" go into the "dying" state,
            if status == 10:
                return True
            return False

        def reproduction(status, sum_neighbours: int):
            #cell turns on if it was off but had exactly two neighbors that were on
            if sum_neighbours//10 == 2 and status == 0:
                return True
            return False

        def make_alive(cell: Cell):
            cell.status_next = 10

        def make_dying(cell: Cell):
            cell.status_next = 1

        def make_dead(cell: Cell):
            cell.status_next = 0

        self.create_rule(is_dying, make_dead)
        self.create_rule(is_alive, make_dying)
        self.create_rule(reproduction, make_alive)

    def make_conway_rules(self):
        def underpopulation(status, sum_neighbours: int):
            if status == 1 and sum_neighbours < 2:
                return True
            return False

        def overpopulation(status, sum_neighbours: int):
            if status == 1 and sum_neighbours > 3:
                return True
            return False

        def stay_alive(status, sum_neighbours: int):
            if status == 1 and sum_neighbours in [2,3]:
                return True
            return False

        def reproduction(status, sum_neighbours: int):
            if status == 0 and sum_neighbours == 3:
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
    def __init__(self, condition: Callable[[int, int], bool], action: Callable[[Cell], None]):
        #Args: condition (callable): function that takes (cell, neighbours) and returns bool
        self.condition = condition
        self.action = action

    def does_apply(self, status, sum_neighbours: int):
        return self.condition(status, sum_neighbours)

    def apply_rule(self, cell: Cell):
        self.action(cell)

if __name__ == '__main__':
    from grid import Grid
    ruleset_test = RuleSet(conway=True)
    grid = Grid(width=5, height=5, ruleset=ruleset_test)
    grid.grid[2][2].status_actual = 1
    grid.grid[2][1].status_actual = 1
    grid.grid[1][2].status_actual = 1
    print(grid)
    for x in range(grid.width):
        for y in range(grid.height):
            neighbours = grid.get_neighbours(grid.grid[y][x])
            result = ruleset_test.apply_rules(cell=grid.grid[y][x], neighbours=neighbours)
    grid.next_turn(ruleset_test)
    print(grid)