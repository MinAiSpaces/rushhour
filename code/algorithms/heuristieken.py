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