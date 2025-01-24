import copy

from code.classes import Vehicle, Board

def free_carter(board: Board) -> int | None:
    """
    Checks if the path for carter is free to end the game.
    Return the steps if carter can reach the finish.
    """
    carter: Vehicle = board.vehicles['X']
    available_moves: int = board.check_move_forwards(carter)

    # check if carter can move to finish
    if (carter.location[1][0] + available_moves) == (board.size - 1):
        return available_moves


def all_max_moves(board: Board) -> list[tuple[Vehicle, int]]:
    """
    Returns only the largest possible moves of all Vehicles on the board
    as a list of moves.
    """
    max_moves: list[tuple[Vehicle, int]] = []

    for vehicle in board.vehicles.values():

            # check maximal forward movement
            move_forwards = board.check_move_forwards(vehicle)
            if move_forwards > 0:
                 max_moves.append((vehicle, move_forwards))

            # check maximal backward movement
            move_backwards = board.check_move_backwards(vehicle)
            if move_backwards > 0:
                 max_moves.append((vehicle, -move_backwards))

    return max_moves


def check_useful_move(board: Board, vehicle: Vehicle, steps: int) -> bool:
    """
    Checks for changes to the available moves after the move of 'vehicle' with
    'steps' length is performed. Returns True if new moves become available.
    """
    new_moves: list[tuple[Vehicle, int]] = []
    check_board = copy.deepcopy(board)

    moves_before = check_board.check_available_moves()
    check_board.move_vehicle(vehicle, steps)
    moves_after = check_board.check_available_moves()

    # find the differnce in available moves
    differences = list(set(moves_after) - set(moves_before))

     # remove the moved vehicle from differences
    for move in differences:
         if move[0] != vehicle:
              new_moves.append(move)

    if len(new_moves) > 0:
         return True

    return False