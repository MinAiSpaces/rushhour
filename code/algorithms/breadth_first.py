import queue
import random
import copy

from code.classes import Board, Vehicle


class BreadthFirst:
    """
    This class explores all possible Board configurations by performing a Breadth First
    Search algorithm, starting from an initial Board state. It maintains a queue of
    Board states, generates child states for valid moves, and continues the search
    until a solution is found.
    """
    def __init__(self, initial_board: Board) -> None:
        """
        Initializes the Breadth First Search algorithm with a specified Board state,
        setting up a queue of Board states where the input Board serves as the initial
        state.
        """
        self.initial_board = initial_board

        # add the initial board state to the queue
        self.states = queue.Queue()
        self.states.put(self.initial_board)

        self.solution = None

    def get_next_state(self):
        """
        Gets the next state from the list of states.
        """
        return self.states.get()

    def build_children(self, board: Board) -> None:
        """
        Generates all possible child states from the current Board state and appends
        them to the list of states. Each child state represents the Board configuration
        after a valid move by a Vehicle.
        """
        possible_moves: list[tuple[Vehicle, int]] = board.check_available_moves()

        # avoid the same vehicle always moving forward and backward
        random.shuffle(possible_moves)

        # add a new board instance to the queue for each valid move
        for vehicle, steps in possible_moves:
            new_board = copy.deepcopy(board)

            # make the valid move in the new board instance
            vehicle = new_board.vehicles[vehicle.name]
            new_board.move_vehicle(vehicle, steps)

            self.states.put(new_board)

    def run(self) -> None:
        """
        Runs the algorithm until all possible Board states are visited or a solution
        is found.
        """
        while not self.states.empty():
            current_board = self.get_next_state()

            # stop if we find a solution
            if current_board.check_game_finished():
                break

            self.build_children(current_board)

        self.solution = current_board