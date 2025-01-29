import queue
import copy
import os

import numpy as np

from code.classes import Board, Mover, CARTER_NAME
from code.utils import write_board_state_to_csv, write_moves_to_csv
from .heuristics import free_carter, all_max_moves, check_useful_move
from code.helpers import get_intermediate_states_path


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
        self.queue.put((initial_state, []))
        self.max_queue_size = 1

        self.seen_states: set[tuple[tuple[object]]] = set()
        self.solution = None
        self.moves: list[tuple[str, int]] = []

    def build_children(
            self, next_state: Board,
            move_history: list[tuple[str, int]],
            max_moves: bool,
            useful_move: bool
        ) -> None:
        """
        Generates all possible child states from the picked Board state and adds them
        to the queue of states if not seen earlier. Each child state represents the
        Board configuration after a valid move by a Vehicle. Also accepts heuristics for
        max_moves (only the largest possible moves) and useful_move (checks if more moves
        become available).
        """
        mover = Mover(next_state)

        if max_moves:
            possible_moves: list[tuple[str, int]] = all_max_moves(next_state)
        else:
            possible_moves: list[tuple[str, int]] = mover.get_all_available_moves()

        # add a new board instance to the queue for each unseen valid move
        for move in possible_moves:

            if useful_move and not check_useful_move(next_state, move[0], move[1]):
                continue

            child_state = copy.deepcopy(next_state)
            new_mover = Mover(child_state)

            # make the valid move in the new board instance
            new_mover.move_vehicle(move)

            # https://www.geeksforgeeks.org/how-to-fix-the-typeerror-unhashable-type-numpy-ndarray/
            if tuple(map(tuple, child_state.locations)) not in self.seen_states:
                self.seen_states.add(tuple(map(tuple, child_state.locations)))
                self.queue.put((child_state, move_history + [move]))

                if len(self.seen_states) % 50000 == 0:
                    intermediate_states_path = get_intermediate_states_path()
                    os.makedirs(intermediate_states_path, exist_ok=True)


                    state_file_path = os.path.join(intermediate_states_path, f'BreadthFirst_state_{len(self.seen_states)}')
                    vehicles = child_state.vehicles.values()
                    write_board_state_to_csv(state_file_path, vehicles)

                    moves_file_path = os.path.join(intermediate_states_path, f'BreadthFirst_moves_{len(self.seen_states)}')
                    moves = move_history + [move]
                    write_moves_to_csv(moves_file_path, moves)
                    print(f'saved progress at {len(self.seen_states)} seen states')

                # keep track of statistics
                if self.queue.qsize() > self.max_queue_size:
                    self.max_queue_size = self.queue.qsize()

    def run(self,
            finish: np.ndarray=None,
            max_moves: bool=False,
            useful_move: bool=False
        ) -> None:
        """
        Runs the algorithm until all possible Board states are visited or a solution
        is found.
        Solution is is_finished method unless a np.ndarray is given.
        """
        while not self.queue.empty():
            next_state, move_history = self.queue.get()

            if np.any(finish):

                # stop if we find the finish
                if np.array_equal(next_state.locations, finish):
                    self.solution = next_state
                    self.moves: list[tuple[str, int]] = move_history

                    print('Step Refiner: state found')

                    break

            else:

                # make the final move when carter can finish the game in one move
                if free_carter(next_state):
                    steps: int = free_carter(next_state)
                    mover = Mover(next_state)
                    move = (CARTER_NAME, steps)

                    mover.move_vehicle(move)
                    move_history.append(move)

                    self.solution = next_state
                    self.moves: list[tuple[str, int]] = move_history

                    break

            self.build_children(next_state, move_history, max_moves, useful_move)

        if not self.solution:
            print('No solution found')
