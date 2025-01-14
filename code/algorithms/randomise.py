import random

from code.classes import Vehicle, Board


def random_from_all_available_valid(board: Board) -> None:
    """
    Makes random moves until carter is in front of the exit and the game is finished.

    Picks a move at random from all available valid moves
    """
    while not board.check_game_finished():
        vehicle, steps = random.choice(board.check_available_moves())
        board.move_vehicle(vehicle, steps)


def random_vehicle_first(board: Board) -> None:
    """
    Makes random moves until carter is in front of the exit and the game is finished.

    Picks a random vehicle from all vehicle with valid moves first
    then picks number of valid steps to move for that vehicle
    """
    while not board.check_game_finished():
        vehicle_moves = {}

        for vehicle, steps in board.check_available_moves():
            vehicle_moves.setdefault(vehicle, []).append(steps)

        random_vehicle = random.choice(list(vehicle_moves.keys()))
        steps = random.choice(vehicle_moves[random_vehicle])

        board.move_vehicle(random_vehicle, steps)

