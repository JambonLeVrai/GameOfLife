from dataclasses import dataclass
#from grid import Grid

min_status = 0
max_status = 1

@dataclass
class Cell:
    x: int
    y: int
    status_actual: int = 0
    status_next: int = 0
    color: tuple[int, int, int] = (255,255,255)

    def __post_init__(self):
        if (self.status_actual > max_status) or (self.status_actual < min_status):
            raise ValueError(
            f"status_actual={self.status_actual} outside the interval [{min_status}, {max_status}]"
        )
def __repr__(self):
    return f"Cell(x:{self.x}, y:{self.y}, actual status: {self.status_actual}, next turn status: {self.status_next})"


if __name__ == '__main__':
    cell = Cell(
        x=1,
        y=2,
        status_actual=3,
        status_next=0,
        color=(0, 0, 0)
    )
    print(cell)