import queue
import copy

import numpy as np

from code.classes import Board, Vehicle


class BreadthFirst:
    """
    This class explores all possible Board configurations by performing a Breadth First
    Search algorithm, starting from an initial Board state. It maintains a queue and
    archive of Board states, generates child states for valid moves, and continues the
    search until a solution is found.
    """
    def __init__(self, initial_state: Board) -> None:
        """
        Initializes the Breadth First Search algorithm with a specified Board state,
        setting up a queue of Board states where the input Board serves as the initial
        state.
        """
        self.queue = queue.Queue()
        self.queue.put(initial_state)

        self.seen_states: set[tuple[tuple[object]]] = set()
        self.solution = None

    def build_children(self, next_state: Board) -> None:
        """
        Generates all possible child states from the picked Board state and adds them
        to the queue of states if not seen earlier. Each child state represents the
        Board configuration after a valid move by a Vehicle.
        """
        possible_moves: list[tuple[Vehicle, int]] = next_state.check_available_moves()

        # add a new board instance to the queue for each unseen valid move
        for vehicle, steps in possible_moves:
            child_state = copy.deepcopy(next_state)

            # make the valid move in the new board instance
            vehicle = child_state.vehicles[vehicle.name]
            child_state.move_vehicle(vehicle, steps)

            # https://www.geeksforgeeks.org/how-to-fix-the-typeerror-unhashable-type-numpy-ndarray/
            if tuple(map(tuple, child_state.locations)) not in self.seen_states:
                self.seen_states.add(tuple(map(tuple, child_state.locations)))
                self.queue.put(child_state)

    def run(self, finish: np.array = None) -> None:
        """
        Runs the algorithm until all possible Board states are visited or a solution
        is found.
        Solution is check_game_finished method unless a np.array is given.
        """
        while not self.queue.empty():
            next_state = self.queue.get()

            # stop if we find a solution
            if np.any(finish):
                if np.array_equal(next_state.locations, finish):
                    print('state found')
                    break

            else:
                if next_state.check_game_finished():
                    break

            self.build_children(next_state)

        self.solution = next_state