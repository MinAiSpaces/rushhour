import numpy as np
import heapq
import copy
import random
from typing import Callable

from code.classes import Board, CARTER_NAME, Mover, Game, Direction


def num_blocking_vehicles(state: Board) -> int:
    """
    Counts the number of vehicles directly blocking Carter in the front.
    """
    carter_row_num = state.vehicles[CARTER_NAME].start_row
    carter_row = state.locations[carter_row_num]

    idx_after_carter = state.vehicles[CARTER_NAME].location[-1][0] + 1

    return len({carter_row[i] for i in range(idx_after_carter, state.size) if carter_row[i] != 0})


def num_two_blocking_vehicles(state: Board) -> int:
    """
    Counts the number of vehicles directly blocking Carter in the front and the
    number of vehicles blocking these.
    """
    carter_row_num = state.vehicles['X'].start_row
    carter_row: np.ndarray[object] = state.locations[carter_row_num]
    idx_after_carter = state.vehicles['X'].location[-1][0] + 1

    first_blocking_vehicles = {carter_row[i] for i in range(idx_after_carter, state.size) if carter_row[i] != 0}
    second_blocking_vehicles = 0

    for first_blocking_vehicle in first_blocking_vehicles:
        if state.check_move_forwards(state.vehicles[first_blocking_vehicle]) == 0:
            second_blocking_vehicles += 1
        if state.check_move_backwards(state.vehicles[first_blocking_vehicle]) == 0:
            second_blocking_vehicles += 1

    return len(first_blocking_vehicles) + second_blocking_vehicles


class AStar:
    """
    This class explores Board configurations by performing a A* algorithm, starting
    from an initial Board state. It maintains a priority queue of to be visisted
    Board states and an archive of seen Board states. It generates child states for
    valid moves and continues the search by selecting states with the lowest score
    based on depth and heuristics until a solution is found.
    """
    def __init__(self, initial_state: Board, heuristic: Callable[[Board], int]) -> None:
        """
        Initializes the A* algorithm with a specified Board state, setting up a
        queue of Board states where the input Board serves as the initial state.
        """
        self.queue = []
        self.heuristic = heuristic

        # add the input board with its score, depth, and empty move history to the heap queue
        heapq.heappush(self.queue, (self.heuristic(initial_state), 0, random.random(), initial_state, []))

        self.seen_states: set[tuple[tuple[object]]] = set()
        self.solution = None
        self.moves: list[tuple[str, int]] = []

    def build_children(self, next_state: Board, depth: int, current_moves: list[tuple[str, int]]) -> None:
        """
        Generates all possible child states from the picked Board state and adds them
        to the heap queue of states if not seen earlier. Each child state represents
        the Board configuration after a valid move by a Vehicle.
        """
        mover = Mover(next_state)
        possible_moves: list[tuple[str, int]] = mover.get_all_available_moves()

        # add a new board instance to the heap queue for each unseen valid move
        for move in possible_moves:
            child_state = copy.deepcopy(next_state)
            new_mover = Mover(child_state)

            # make the valid move in the state
            new_mover.move_vehicle(move)

            # https://www.geeksforgeeks.org/how-to-fix-the-typeerror-unhashable-type-numpy-ndarray/
            if tuple(map(tuple, child_state.locations)) not in self.seen_states:
                self.seen_states.add(tuple(map(tuple, child_state.locations)))

                # add the state with its score to the heap queue
                score = depth + 1 + self.heuristic(child_state)
                heapq.heappush(self.queue, (score, depth + 1, random.random(), child_state, current_moves + [move]))

    def run(self) -> None:
        """
        Runs the algorithm until all possible Board states are visited or a solution
        is found.
        """
        while self.queue:

            # pop the state with the lowest score; pick randomly if tied
            score, depth, random_boundary, current_state, move_history = heapq.heappop(self.queue)

            if Game.is_finished(current_state):
                self.solution = current_state
                self.moves = move_history
                break

            self.build_children(current_state, depth, move_history)

        self.solution = current_state
