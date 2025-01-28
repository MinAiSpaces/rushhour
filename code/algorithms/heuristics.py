import copy

from code.classes import Vehicle, Board, Mover, Direction, CARTER_NAME


def free_carter(board: Board) -> int | None:
     """
     Checks if the path for carter is free to end the game.
     Return the steps if carter can reach the finish.
     """
     mover = Mover(board)

     carter: Vehicle = board.vehicles[CARTER_NAME]
     carter_max_steps_forward: int = mover.get_vehicle_max_steps(CARTER_NAME, Direction.FORWARDS)

     # check if carter can move to finish
     if (carter.location[1][0] + carter_max_steps_forward) == (board.size - 1):
          return carter_max_steps_forward


def all_max_moves(board: Board) -> list[tuple[str, int]]:
     """
     Returns only the largest possible moves of all Vehicles on the board
     as a list of moves.
     """
     mover = Mover(board)

     max_moves: list[tuple[str, int]] = []

     for vehicle_name in board.vehicles:

               # check maximal forward movement
               move_forwards = mover.get_vehicle_max_steps(vehicle_name, Direction.FORWARDS)
               if move_forwards > 0:
                    max_moves.append((vehicle_name, move_forwards))

               # check maximal backward movement
               move_backwards = mover.get_vehicle_max_steps(vehicle_name, Direction.BACKWARDS)
               if move_backwards > 0:
                    max_moves.append((vehicle_name, -move_backwards))

     return max_moves


def check_useful_move(board: Board, vehicle_name: str, steps: int) -> bool:
     """
     Checks for changes to the available moves after the move of 'vehicle' with
     'steps' length is performed. Returns True if at least one new move,
     except moves including the vehicle that was just moved, becomes available.
     """
     check_board = copy.deepcopy(board)

     mover = Mover(check_board)
     moves_before = mover.get_all_available_moves()
     mover.move_vehicle((vehicle_name, steps))
     moves_after = mover.get_all_available_moves()

     # find the difference in available moves
     differences = list(set(moves_after) - set(moves_before))

     for move in differences:
          if move[0] != vehicle_name:
               return True

     return False
