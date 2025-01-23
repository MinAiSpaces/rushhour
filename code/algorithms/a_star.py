import numpy as np
import heapq
import copy
import random

from code.classes import Board, Vehicle


def num_blocking_vehicles(state: Board) -> int:
    """
    Counts the number of vehicles directly blocking Carter in the front.
    """
    carter_row_num = state.vehicles['X'].start_row
    carter_row: np.ndarray[object] = state.locations[carter_row_num]

    idx_after_carter = state.vehicles['X'].location[-1][0] + 1

    return len({carter_row[i] for i in range(idx_after_carter, len(carter_row)) if carter_row[i] != 0})


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
        elif state.check_move_backwards(state.vehicles[first_blocking_vehicle]) == 0:
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
    def __init__(self, initial_state: Board) -> None:
        """
        Initializes the A* algorithm with a specified Board state, setting up a
        queue of Board states where the input Board serves as the initial state.
        """
        self.queue = []

        # add the input board with its score and depth to the heap queue
        heapq.heappush(self.queue, (num_two_blocking_vehicles(initial_state), 0, random.random(), initial_state))

        self.seen_states: set[tuple[tuple[object]]] = set()
        self.solution = None

    def build_children(self, next_state: Board, depth: int) -> None:
        """
        Generates all possible child states from the picked Board state and adds them
        to the heap queue of states if not seen earlier. Each child state represents
        the Board configuration after a valid move by a Vehicle.
        """
        possible_moves: list[tuple[Vehicle, int]] = next_state.check_available_moves()

        # add a new board instance to the heap queue for each unseen valid move
        for vehicle, steps in possible_moves:
            child_state = copy.deepcopy(next_state)

            # make the valid move in the state
            vehicle = child_state.vehicles[vehicle.name]
            child_state.move_vehicle(vehicle, steps)

            # https://www.geeksforgeeks.org/how-to-fix-the-typeerror-unhashable-type-numpy-ndarray/
            if tuple(map(tuple, child_state.locations)) not in self.seen_states:
                self.seen_states.add(tuple(map(tuple, child_state.locations)))

                # add the state with its score to the heap queue
                score = depth + 1 + num_two_blocking_vehicles(child_state)
                heapq.heappush(self.queue, (score, depth + 1, random.random(), child_state))

    def run(self) -> None:
        """
        Runs the algorithm until all possible Board states are visited or a solution
        is found.
        """
        while self.queue:

            # pop the state with the lowest score; pick randomly if tied
            score, depth, random_boundary, current_state = heapq.heappop(self.queue)

            if current_state.check_game_finished():
                break

            self.build_children(current_state, depth)

        self.solution = current_state
