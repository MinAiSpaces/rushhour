from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class VehicleMoveViolationError(Exception):
    def __init__(self):
        super().__init__('Vehicle move violation. Vehicle cannot change row or column.')


class Vehicle:
    """
    Vehicle represents the cars (length 2) and trucks (length 3) on the board.
    """
    def __init__(self, name: str, orientation: Orientation, start_col: int, start_row: int, length: int) -> None:
        """
        Uses start_col and start_row only to calculate the start location of the Vehicle.
        Saves the location of the Vehicle in a list of tuples containing all the
        coordinates the Vehicle occupies.
        is_carter keeps track if this Vehicle is the red car.
        """
        self.name = name
        self.orientation = orientation
        self.start_col = start_col
        self.start_row = start_row
        self.length = length
        self.is_carter: bool = name == 'X'
        self.location: list[tuple[int, int]] = []

        self.update_location(start_col, start_row)

    def update_location(self, col: int, row: int) -> None:
        """
        Updates the location of the Vehicle starting at row, col.
        Col and row represent the coordinates of the back of the car.
        """
        location = []

        # save all coordinates of the vehicle
        for i in range(self.length):
            if self.orientation == Orientation.HORIZONTAL:
                location.append((row, col + i))
            else:
                location.append((row + i, col))

        self.location = location
