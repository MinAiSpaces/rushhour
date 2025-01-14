import random

from classes import Vehicle, Board

def random_moves(board: Board) -> None:
    """
    Makes random moves until carter is in front of the exit and the game is finished.
    """
    while not board.check_game_finished():
        available_moves: list[tuple[Vehicle, int]] = board.check_available_moves()
        vehicle, steps = random.choice(available_moves)
        board.move_vehicle(vehicle, steps)