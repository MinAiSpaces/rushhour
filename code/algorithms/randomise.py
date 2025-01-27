import random

from code.classes import Board, Game, CARTER_NAME
from .heuristics import free_carter, all_max_moves


def random_from_all_available_valid(game: Game) -> None:
    """
    Makes random moves until carter is in front of the exit and the game is finished.

    Picks a move at random from all available valid moves
    """
    while not Game.is_finished(game.board):
        move: tuple[str, int] = random.choice(game.get_all_available_moves())

        game.make_move(move)


def random_vehicle_first(game: Game) -> None:
    """
    Makes random moves until carter is in front of the exit and the game is finished.

    Picks a random vehicle from all vehicle with valid moves first
    then picks number of valid steps to move for that vehicle
    """
    while not Game.is_finished(game.board):
        vehicle_moves: set[str, list[int]] = {}

        for vehicle, steps in game.get_all_available_moves():
            vehicle_moves.setdefault(vehicle, []).append(steps)

        random_vehicle = random.choice(list(vehicle_moves.keys()))
        steps = random.choice(vehicle_moves[random_vehicle])

        game.make_move((random_vehicle, steps))


def all_available_valid_finish_check(game: Game) -> None:
    """
    Makes random moves until carter can finish the game.
    Picks a move at random from all available valid moves unless moving carter finishes the game.
    """
    while not Game.is_finished(game.board):
        finish_game: int | None = free_carter(game.board)

        if finish_game:
            game.make_move((CARTER_NAME, finish_game))
        else:
            move: tuple[str, int] = random.choice(game.get_all_available_moves())
            game.make_move(move)


def all_max_moves_finish_check(game: Game) -> None:
    """
    Makes random moves until carter can finish the game.
    Picks a move at random from all maximum moves unless moving carter finishes the game.
    """
    while not Game.is_finished(game.board):
        finish_game: int | None = free_carter(game.board)

        if finish_game:
            game.make_move((CARTER_NAME, finish_game))
        else:
            move: tuple[str, int] = random.choice(all_max_moves(game.board))
            game.make_move(move)
