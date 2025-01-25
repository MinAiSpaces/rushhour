from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from .vehicle import Vehicle, Orientation


EMPTY_SPOT = 0


class BoardPlacementError(ValueError):
    def __init__(self, vehicle_name: str, message: str):
        super().__init__(f"Vehicle '{vehicle_name}': {message}")


class BoardPlacementOutOfBoundsError(BoardPlacementError):
    def __init__(self, vehicle_name: str):
        super().__init__(
            vehicle_name,
            'placement is out of bounds')


class BoardPlacementOccupiedError(BoardPlacementError):
    def __init__(self, vehicle_name: str):
        super().__init__(
            vehicle_name,
            'placement is on top of another vehicle'
        )


class BoardVehicleNameExistError(BoardPlacementError):
    def __init__(self, vehicle_name: str):
        super().__init__(
            vehicle_name,
            'a vehicle with this name already exists'
        )


class BoardVehicleCarterOrientationError(BoardPlacementError):
    def __init__(self, vehicle_name: str):
        super().__init__(
            vehicle_name,
            'Carter can only be placed horizontally'
        )


@dataclass
class Board:
    """
    Initializes the Board with a size, applicable to both its width and length.
    Also sets up a dictionary to store vehicles (vehicle names as keys and
    vehicle objects as values), a list to track the movement steps of vehicles
    (vehicle names and step sizes as tuples), and an empty 2-D array to
    represent the Board's layout.
    """
    size: int
    vehicles: dict[str, 'Vehicle'] = field(default_factory=dict, init=False)
    locations: NDArray[int | str] = field(init=False)  # type: ignore[type-var]

    def __post_init__(self):
        self.locations = np.zeros((self.size, self.size), dtype='object')

    def add_vehicle(self, vehicle: Vehicle) -> None:
        """
        Adds a Vehicle to the Board by storing it in the vehicles dictionary
        and updating the Board's layout to include the Vehicle's position.

        Raises an exception:
            - if the vehicle is place outside the board
            - if the vehicle is placed on top of another vehicle
        """
        if vehicle.name in self.vehicles:
            raise BoardVehicleNameExistError(vehicle.name)

        if (
            vehicle.is_carter
            and not vehicle.orientation == Orientation.HORIZONTAL
        ):
            raise BoardVehicleCarterOrientationError(vehicle.name)

        cols, rows = zip(*vehicle.location)

        if not (
            cols[0] >= 0
            and rows[0] >= 0
            and cols[-1] < self.size
            and rows[-1] < self.size
        ):
            raise BoardPlacementOutOfBoundsError(vehicle.name)

        if np.any(self.locations[rows, cols]):
            raise BoardPlacementOccupiedError(vehicle.name)

        self.vehicles[vehicle.name] = vehicle
        self.update_state(vehicle, True)

    def update_state(self, vehicle: Vehicle, new=False) -> None:
        """
        Updates the state of the board by storing either 0 or a 'vehicle name'
        at the supplied coordinates.

        If new == False:
            - First 'removes' vehicle from the board by replacing its location
              on the board with zeros,
            - then storing the vehicle name at the new coordinates
        else:
            - not going to remove the vehicle from the board first
        """
        if not new:
            self.locations[self.locations == vehicle.name] = 0

        for col, row in vehicle.location:
            self.locations[row, col] = vehicle.name
