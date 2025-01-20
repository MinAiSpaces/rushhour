import copy

from code.classes import Board, Vehicle


class DepthFirst:
    """
    This class explores all possible Board configurations by performing a Depth First
    Search algorithm, starting from an initial Board state. It maintains a stack of
    Board states, generates child states for valid moves, and continues the search
    until a solution is found.
    """
    def __init__(self, initial_board: Board) -> None:
        """
        Initializes the Depth First Search algorithm with a specified Board state,
        setting up a stack of Board states where the input Board serves as the initial
        state.
        """
        self.initial_board = initial_board
        self.states = [copy.deepcopy(self.initial_board)]
        self.solution = None

    def get_next_state(self) -> Board:
        """
        Gets the next state from the list of states.
        """
        return self.states.pop()

    def build_children(self, board: Board) -> None:
        """
        Generates all possible child states from the current Board state and appends
        them to the list of states. Each child state represents the Board configuration
        after a valid move by a Vehicle.
        """
        possible_moves: list[tuple[Vehicle, int]] = board.check_available_moves()

        # add a new board instance to the stack for each valid move
        for vehicle, steps in possible_moves:
            new_board = copy.deepcopy(board)

            # make the valid move in the new board instance
            vehicle = new_board.vehicles[vehicle.name]
            new_board.move_vehicle(vehicle, steps)

            self.states.append(new_board)

    def run(self) -> None:
        """
        Runs the algorithm until all possible Board states are visited.
        """
        while self.states:
            current_board = self.get_next_state()

            # stop if we find a solution
            if current_board.check_game_finished():
                break

            self.build_children(current_board)

        self.solution = current_board