import numpy as np
import heapq
import random
from typing import Callable

from code.classes import Board, CARTER_NAME, Mover, Direction, Game, Orientation
from code.algorithms import free_carter, all_max_moves


def num_blocking_vehicles(state: Board) -> int:
    """
    Counts the number of vehicles directly blocking Carter in the front.
    """
    carter_row_num = state.vehicles[CARTER_NAME].start_row
    carter_row = state.locations[carter_row_num]

    col_in_front_of_carter = state.vehicles[CARTER_NAME].location[-1][0] + 1

    return len({
        carter_row[i]
        for i in range(col_in_front_of_carter, state.size)
        if carter_row[i] != 0
    })


def num_two_blocking_vehicles(state: Board) -> int:
    """
    Counts the number of vehicles directly blocking Carter in the front and the
    number of vehicles blocking these.
    """
    mover = Mover(state)
    carter_row_num = state.vehicles[CARTER_NAME].start_row
    carter_row: np.ndarray[object] = state.locations[carter_row_num]
    col_in_front_of_carter = state.vehicles[CARTER_NAME].location[-1][0] + 1

    # Set of unique vehicle names in front of Carter
    vehicles_first_degree = {
        carter_row[i]
        for i in range(col_in_front_of_carter, state.size)
        if carter_row[i] != 0
    }
    vehicles_second_degree_counter = 0

    for blocking_vehicle_name in vehicles_first_degree:
        if mover.get_vehicle_max_steps(blocking_vehicle_name, Direction.FORWARDS) == 0:
            vehicles_second_degree_counter += 1
        if mover.get_vehicle_max_steps(blocking_vehicle_name, Direction.BACKWARDS) == 0:
            vehicles_second_degree_counter += 1

    return len(vehicles_first_degree) + vehicles_second_degree_counter


class AStar:
    """
    This class explores Board configurations by performing a A* algorithm, starting
    from an initial Board state. It maintains a priority queue of to be visisted
    Board states and an archive of seen Board states. It generates child states for
    valid moves and continues the search by selecting states with the lowest score
    based on depth and heuristics until a solution is found.
    """
    def __init__(self, initial_state: Board, heuristic: Callable[[Board], int]=None) -> None:
        """
        Initializes the A* algorithm with a specified Board state, setting up a
        queue of Board states where the input Board serves as the initial state.
        """
        self.queue = []
        self.heuristic = heuristic

        # add the input board with its score, depth, and empty move history to the heap queue
        heapq.heappush(self.queue, (self.heuristic(initial_state), 0, random.random(), initial_state, []))
        self.max_queue_size = 1

        self.seen_states: set[tuple[tuple[object]]] = set()
        self.solution = None
        self.moves: list[tuple[str, int]] = []

    def build_children(
            self,
            next_state: Board,
            depth: int,
            current_moves: list[tuple[str, int]],
            max_moves: bool
        ) -> None:
        """
        Generates all possible child states from the picked Board state and adds them
        to the heap queue of states if not seen earlier. Each child state represents
        the Board configuration after a valid move by a Vehicle.
        """
        mover = Mover(next_state)

        if max_moves:
            possible_moves: list[tuple[str, int]] = all_max_moves(next_state)
        else:
            possible_moves: list[tuple[str, int]] = mover.get_all_available_moves()

        # add a new board instance to the heap queue for each unseen valid move
        for move in possible_moves:

            # create new board as child_state
            data: list[tuple[str, Orientation, int, int, int]] = []
            for vehicle in next_state.vehicles.values():
                data.append((vehicle.name, vehicle.orientation, vehicle.location[0][0], vehicle.location[0][1], vehicle.length))

            child_state = Game.setup_board(Board(next_state.size), data)

            new_mover = Mover(child_state)

            # make the valid move in the state
            new_mover.move_vehicle(move)

            # https://www.geeksforgeeks.org/how-to-fix-the-typeerror-unhashable-type-numpy-ndarray/
            if tuple(map(tuple, child_state.locations)) not in self.seen_states:
                self.seen_states.add(tuple(map(tuple, child_state.locations)))

                # add the state with its score to the heap queue
                score = depth + 1 + self.heuristic(child_state)
                heapq.heappush(self.queue, (score, depth + 1, random.random(), child_state, current_moves + [move]))

                # keep track of statistics
                if len(self.queue) > self.max_queue_size:
                    self.max_queue_size = len(self.queue)

    def run(self, max_moves: bool=False) -> None:
        """
        Runs the algorithm until all possible Board states are visited or a solution
        is found.
        """
        while self.queue:

            # pop the state with the lowest score; pick randomly if tied
            score, depth, random_boundary, current_state, move_history = heapq.heappop(self.queue)

            # make the final move when carter can finish the game in one move
            if free_carter(current_state):
                steps: int = free_carter(current_state)
                mover = Mover(current_state)
                move = (CARTER_NAME, steps)

                mover.move_vehicle(move)
                move_history.append(move)

                self.solution = current_state
                self.moves: list[tuple[str, int]] = move_history

                break

            self.build_children(current_state, depth, move_history, max_moves)

        self.solution = current_state
