import random

from classes import Vehicle, Board

def random_moves(board: Board):
    while not board.check_game_finished():
        available_moves = board.check_available_moves()
        vehicle, steps = random.choice(available_moves)
        board.move_vehicle(vehicle, steps)