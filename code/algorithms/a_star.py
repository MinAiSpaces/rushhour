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


class AStar:
    """

    """
    def __init__(self, initial_state: Board) -> None:
        """

        """
        self.queue = []
        heapq.heappush(self.queue, (num_blocking_vehicles(initial_state), 0, random.random(), initial_state))

        self.seen_states = set()
        self.solution = None

    def build_children(self, next_state: Board, depth: int) -> None:
        """

        """
        possible_moves: list[tuple[Vehicle, int]] = next_state.check_available_moves()

        # add a new board instance to the heap queue for each unseen valid move
        for vehicle, steps in possible_moves:
            child_state = copy.deepcopy(next_state)

            # make the valid move in the new board instance
            vehicle = child_state.vehicles[vehicle.name]
            child_state.move_vehicle(vehicle, steps)

            # https://www.geeksforgeeks.org/how-to-fix-the-typeerror-unhashable-type-numpy-ndarray/
            if tuple(map(tuple, child_state.locations)) not in self.seen_states:
                self.seen_states.add(tuple(map(tuple, child_state.locations)))

                total_score = depth + num_blocking_vehicles(child_state)

                # add the state with its cost and heur to the heap queue
                heapq.heappush(self.queue, (total_score, depth + 1, random.random(), child_state))
                score = depth + 1 + num_blocking_vehicles(child_state)

    def run(self) -> None:
        """

        """
        while self.queue:

            # pop the state with the smallest cost and heur
            total_score, depth, random_boundary, current_state = heapq.heappop(self.queue)

            if current_state.check_game_finished():
                break

            self.build_children(current_state, depth)

        self.solution = current_state
