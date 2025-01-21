from code.classes import Vehicle, Board

def free_carter(board: Board) -> int | None:
    """
    Check if the path for carter is free to end the game.
    Return the steps if carter can reach the finish.
    """
    carter: Vehicle = board.vehicles['X']
    available_moves: int = board.check_move_forwards(carter)

    # check if carter can move to finish
    if (carter.location[1][0] + available_moves) == (board.size - 1):
        return available_moves


def all_max_moves(board: Board) -> list[tuple[Vehicle, int]]:
    max_moves = []

    for vehicle in board.vehicles.values():

            # check forward movement
            move_forwards = board.check_move_forwards(vehicle)
            if move_forwards > 0:
                 max_moves.append((vehicle, move_forwards))

            # check backward movement
            move_backwards = board.check_move_backwards(vehicle)
            if move_backwards > 0:
                 max_moves.append((vehicle, -move_backwards))

    return max_moves


def check_useful_move(board: Board, move: tuple[Vehicle, int]):

    moves_before = board.check_available_moves()
    board.move_vehicle(move[0], move[1])
    moves_after = board.check_available_moves()

    new_moves = list(set(moves_after) - set(moves_before))


    return new_moves