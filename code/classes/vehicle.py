from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Vehicle:
    def __init__(self, name: str, orientation: object, start_col: int, start_row: int, length: int):
        """
        Uses start_col and start_row only to calculate the start location of the vehicle.
        Saves the location of the vehicle in a list of tuples containing all the
        coordinates the vehicle occupies.
        Is_carter keeps track of the red car.
        """
        self.name = name
        self.orientation = orientation
        self.start_col = start_col
        self.start_row = start_row
        self.length = length
        self.is_carter = name == 'X'
        self.location = []

        self.update_location(start_col, start_row)

    def update_location(self, col: int, row: int):
        """
        Updates the location of the Vehicle starting at row,col.
        Col and row represent the coordinates of the back of the car.
        """
        location = []

        # save all coordinates of the vehicle
        for i in range(self.length):
            if self.orientation == Orientation.HORIZONTAL:
                location.append((row, col + i))
            else:
                location.append((row + i, col))

        self.location: list[tuple] = location
