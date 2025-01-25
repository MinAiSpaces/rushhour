from dataclasses import dataclass
from enum import Enum

import numpy as np

from .board import Board, EMPTY_SPOT
from .vehicle import Orientation


class Direction(Enum):
    FORWARDS = 'FORWARDS'
    BACKWARDS = 'BACKWARDS'


class MoveError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)


class MoveOutOfBoundsError(MoveError):
    def __init__(self):
        super().__init__('Move would place vehicle out of bounds')


class MoveStepIsZeroError(MoveError):
    def __init__(self):
        super().__init__('Move cannot have a step of 0')


class MoveVehicleNotExistError(MoveError):
    def __init__(self):
        super().__init__('Trying to move a vehicle that does not exist')


class MoveVehicleBlockedError(MoveError):
    def __init__(self):
        super().__init__('Move is blocked by another vehicle')


@dataclass
class Mover:
    """
    Mover handles everything regarding moves. It is responsible for move
    validation and execution according to the rules of the game.

    Responsible for:
        - making sure moves are within bounds
        - vehicles not collide with other vehicles
        - updating the board state after a valid move
        - calculating all the available valid moves for the current board state
    """
    board: Board

    def _get_all_moves_vehicle(
        self,
        vehicle_name: str
    ) -> list[tuple[str, int]]:
        """
        Gets a list of all available moves for a particular vehicle
        on the board.

        Checks if vehicles have available moves in both forwards and backwards
        direction.
        """
        all_vehicle_moves: list[tuple[str, int]] = []

        # Get steps forwards
        max_steps_forward = self.get_vehicle_max_steps(
            vehicle_name,
            Direction.FORWARDS
        )

        for steps in range(1, max_steps_forward + 1):
            all_vehicle_moves.append((vehicle_name, steps))

        # Get steps backwards
        max_steps_backward = self.get_vehicle_max_steps(
            vehicle_name,
            Direction.BACKWARDS
        )

        for steps in range(1, max_steps_backward + 1):
            all_vehicle_moves.append((vehicle_name, -steps))

        return all_vehicle_moves

    def get_all_available_moves(
        self,
        vehicle_name: str | None = None
    ) -> list[tuple[str, int]]:
        """
        Gets a list of all available valid moves

        If 'vehicle_name' is provided:
            - only returns available valid moves for particular vehicle
        else:
            - gets all available valid moves for all vehicles on the board
        """
        available_moves: list[tuple[str, int]] = []

        if vehicle_name:
            available_moves = self._get_all_moves_vehicle(vehicle_name)
        else:
            for vehicle_name, vehicle in self.board.vehicles.items():
                available_moves.extend(
                    self._get_all_moves_vehicle(vehicle_name)
                )

        return available_moves

    def get_vehicle_max_steps(
        self,
        vehicle_name: str,
        direction: Direction
    ) -> int:
        """
        Gets the maximum number of steps a vehicle can move in the given
        direction

        Rules:
            - can only move to empty spots immediately in front of
              behind
            - cannot move through or jump over other vehicles
            - cannot move to an occupied spot on the board
            - steps can never be more than difference between board edge
              and vehicle front or vehicle back depending on the direction

        Raises exception if:
            - vehicle does not exist

        If vehicle.orientation is Orientation.HORIZONTAL:
            if direction is Direction.FORWARDS:
                - checks coordinates from the front of the vehicle up until the
                  right side of the board
            else direction is Direction.BACKWARDS:
                - checks coordinates from the back of the vehicle up until the
                  left side of the board
        else vehicle.orientation is Orientation.VERTICAL:
            if direction is Direction.FORWARDS:
                - checks coordinates from the front of the vehicle up until the
                  bottom of the board
            else direction is Direction.BACKWARDS:
                - checks coordinates from the back of the vehicle up until the
                  top of the board

        Uses Numpy for faster value comparison
        """
        board = self.board
        vehicle = self.board.vehicles.get(vehicle_name)

        if vehicle is None:
            raise MoveVehicleNotExistError()

        orientation = vehicle.orientation
        col_vehicle_back, row_vehicle_back = vehicle.location[0]
        col_vehicle_front, row_vehicle_front = vehicle.location[-1]

        if orientation == Orientation.HORIZONTAL:
            if direction == Direction.FORWARDS:
                max_steps = board.size - 1 - col_vehicle_front
                start = col_vehicle_front + 1
                end = start + max_steps
                squares_to_check = board.locations[row_vehicle_back, start:end]
            else:
                max_steps = col_vehicle_back
                start = col_vehicle_back - max_steps
                end = col_vehicle_back
                squares_to_check = board.locations[row_vehicle_back, start:end]

                # Since we're moving backwards we'd like np.argmax() to 'scan'
                # in reverse order
                squares_to_check = np.flip(squares_to_check)
        else:
            if direction == Direction.FORWARDS:
                max_steps = board.size - 1 - row_vehicle_front
                start = row_vehicle_front + 1
                end = start + max_steps
                squares_to_check = board.locations[start:end, col_vehicle_back]
            else:
                max_steps = row_vehicle_back
                start = row_vehicle_back - max_steps
                end = row_vehicle_back
                squares_to_check = board.locations[start:end, col_vehicle_back]

                # Since we're moving backwards we'd like np.argmax() to 'scan'
                # in reverse order
                squares_to_check = np.flip(squares_to_check)

        # Creates boolean array (no collision results in no 'True' values)
        has_collision = np.any(squares_to_check != EMPTY_SPOT)

        # Default 'collision_idx' to max length (no 'True' values)
        collision_at_idx = len(squares_to_check)

        if has_collision:
            # np.argmax() returns the index of the first occurrence of 'True'
            collision_at_idx = np.argmax(squares_to_check != EMPTY_SPOT)

        # Pick whichever is lowest of 'max_steps' or 'collision_at_idx'
        return min(max_steps, collision_at_idx)

    def move_vehicle(self, move: tuple[str, int]) -> None:
        """
        Moves a vehicle on the board

        Only moves vehicle if:
            - vehicle exists
            - move can be made (not blocked or out of bounds)
        """
        vehicle_name, steps = move
        vehicle = self.board.vehicles.get(vehicle_name)

        self.validate_move(move)

        col_back, row_back = vehicle.location[0]

        if vehicle.orientation == Orientation.HORIZONTAL:
            vehicle.update_location(col_back + steps, row_back)
        else:
            vehicle.update_location(col_back, row_back + steps)

        self.board.update_state(vehicle)

    def validate_move(self, move: tuple[str, int]) -> None:
        """
        Validates a move

        Raises exception when:
            - step is 0
            - vehicle does not exist (done in 'get_vehicle_max_steps')
            - the move is blocked or would move the vehicle out of bounds
        """
        vehicle_name, steps = move
        vehicle = self.board.vehicles.get(vehicle_name)

        if steps == 0:
            raise MoveStepIsZeroError()

        direction = Direction.FORWARDS if steps > 0 else Direction.BACKWARDS
        max_steps = self.get_vehicle_max_steps(vehicle_name, direction)

        col_vehicle_front, row_vehicle_front = vehicle.location[-1]
        col_vehicle_back, row_vehicle_back = vehicle.location[0]
        first_board_col = first_board_row = 0
        last_board_col = last_board_row = self.board.size - 1

        if max_steps == 0:
            if direction == Direction.FORWARDS:
                if (
                    vehicle.orientation == Orientation.HORIZONTAL
                    and col_vehicle_front == last_board_col
                ) or (
                    vehicle.orientation == Orientation.VERTICAL
                    and row_vehicle_front == last_board_row
                ):
                    raise MoveOutOfBoundsError()
            elif direction == Direction.BACKWARDS:
                if (
                    vehicle.orientation == Orientation.HORIZONTAL
                    and col_vehicle_back == first_board_col
                ) or (
                    vehicle.orientation == Orientation.VERTICAL
                    and row_vehicle_back == first_board_row
                ):
                    raise MoveOutOfBoundsError()

            raise MoveVehicleBlockedError()

        if abs(steps) > max_steps:
            raise MoveOutOfBoundsError()

