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
            move_forwards = check_move_forwards(vehicle)
            if board.move_forwards > 0:
                 max_moves.append((vehicle, move_forwards))

            move_backwards = board.check_move_backwards(vehicle)
            if board.move_backwards > 0:
                 max_moves.append((vehicle, -move_backwards))
    print(max_moves)
    return max_moves