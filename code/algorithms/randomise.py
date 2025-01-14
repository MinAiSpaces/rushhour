import random


def check_available_moves(board) -> list[tuple[Vehicle, int]]:
    """
    Checks all possible moves for the Board and returns them.
    """

    possible_states = []

    for vehicle in board.values():

        for possible_step in range(1, board.check_move_forwards(vehicle) + 1):
            possible_states.append((vehicle, possible_step))

        for possible_step in range(1, board.check_move_backwards(vehicle) + 1):
            possible_states.append((vehicle, -possible_step))

    return possible_states
