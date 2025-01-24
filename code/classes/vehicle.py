from dataclasses import dataclass, field
from enum import Enum


CARTER_NAME = 'X'


class Orientation(Enum):
    HORIZONTAL = 'H'
    VERTICAL = 'V'


@dataclass
class Vehicle:
    """
    Vehicle represents the cars (length 2) and trucks (length 3) on the board.
    """
    name: str
    orientation: Orientation
    start_col: int
    start_row: int
    length: int
    is_carter: bool = field(default=False)
    location: list[tuple[int, int]] = field(default_factory=list)

    def __post_init__(self):
        self.is_carter = self.name == CARTER_NAME
        self.update_location(self.start_col, self.start_row)

    def update_location(self, col: int, row: int) -> None:
        """
        Updates the location of the Vehicle starting at col, row.
        Col and row represent the coordinates of the back of the car.

        A vehicle keeps a list of coordinates of the grid squares it occupies
        on the board.
        """
        if self.orientation == Orientation.HORIZONTAL:
            self.location = [(col + i, row) for i in range(self.length)]
        else:
            self.location = [(col, row + i) for i in range(self.length)]
