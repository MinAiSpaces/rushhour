from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Vehicle:
    def __init__(self, name, orientation, start_col, start_row, length):
        self.name = name
        self.orientation = orientation
        self.start_col = start_col
        self.start_row = start_row
        self.length = length
        self.is_carter = name == 'X'
        self.location = []

        self.update_location(start_col, start_row)

    def update_location(self, col, row):
        location = []

        for i in range(self.length):
            if self.orientation == Orientation.HORIZONTAL:
                location.append((row, col + i))
            else:
                location.append((row + i, col))

        self.location = location
