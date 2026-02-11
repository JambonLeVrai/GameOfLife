from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int
    status_actual: int = 0
    status_next: int = 0

    def update(self):
        self.status_actual = self.status_next

    def __repr__(self):
        return str(self.status_next)


if __name__ == '__main__':
    cell = Cell(
        x=1,
        y=2,
        status_actual=3,
        status_next=0,
    )
    print(cell)