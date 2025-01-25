import copy

from code.classes import Board, Vehicle


class DepthFirst:
    """
    This class explores all possible Board configurations by performing a Depth First
    Search algorithm, starting from an initial Board state. It maintains a stack of
    to be visited Board states, an archive of seen Board states and applies 'branch
    and bound'. It generates child states for valid moves and continues the search
    until a solution is found.
    """
    def __init__(self, initial_state: Board) -> None:
        """
        Initializes the Depth First Search algorithm with a specified Board state,
        setting up a stack of Board states where the input Board serves as the initial
        state.
        """
        self.stack = [(0, copy.deepcopy(initial_state))]
        self.seen_states: set[tuple[tuple[object]]] = set()
        self.shortest_path = float('inf')
        self.best_solution = None

    def build_children(self, next_state: Board, depth: int) -> None:
        """
        Generates all possible child states from the picked Board state and appends
        them to the stack of states if not seen earlier and within the shortest path.
        Each child state represents the Board configuration after a valid move by a
        Vehicle.
        """
        possible_moves: list[tuple[Vehicle, int]] = next_state.check_available_moves()

        # add new board instances of unseen valid shortest path moves to the stack
        for vehicle, steps in possible_moves:
            child_state = copy.deepcopy(next_state)

            # make the valid move in the state
            vehicle = child_state.vehicles[vehicle.name]
            child_state.move_vehicle(vehicle, steps)

            # https://www.geeksforgeeks.org/how-to-fix-the-typeerror-unhashable-type-numpy-ndarray/
            if tuple(map(tuple, child_state.locations)) not in self.seen_states:
                self.seen_states.add(tuple(map(tuple, child_state.locations)))

                # explore branches within the shortest path found so far
                if depth + 1 <= self.shortest_path:
                    self.stack.append((depth + 1, child_state))

    def run(self) -> None:
        """
        Runs the algorithm until all possible Board states are visited or a solution
        is found.
        """
        while self.stack:

            # get the board instance on top of the stack
            depth, next_state = self.stack.pop()

            # update when a solution is within the shortest path
            if next_state.check_game_finished():
                if depth < self.shortest_path:
                    self.shortest_path = depth
                    self.best_solution = next_state
                continue

            self.build_children(next_state, depth)