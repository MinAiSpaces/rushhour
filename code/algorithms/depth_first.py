import copy

from code.classes import Board, Vehicle


class DepthFirst:
    """
    This class explores all possible Board configurations by performing a Depth First
    Search algorithm, starting from an initial Board state. It maintains a stack and
    archive of Board states, generates child states for valid moves, and continues the
    search until a solution is found.
    """
    def __init__(self, initial_state: Board) -> None:
        """
        Initializes the Depth First Search algorithm with a specified Board state,
        setting up a stack of Board states where the input Board serves as the initial
        state.
        """
        self.states = [copy.deepcopy(initial_state)]
        self.seen_states: set[tuple[tuple[object]]] = set()
        self.solution = None

    def build_children(self, next_state: Board) -> None:
        """
        Generates all possible child states from the picked Board state and appends
        them to the stack of states if not seen earlier. Each child state represents
        the Board configuration after a valid move by a Vehicle.
        """
        possible_moves: list[tuple[Vehicle, int]] = next_state.check_available_moves()

        # add a new board instance to the stack for each valid move
        for vehicle, steps in possible_moves:
            child_state = copy.deepcopy(next_state)

            # make the valid move in the new board instance
            vehicle = child_state.vehicles[vehicle.name]
            child_state.move_vehicle(vehicle, steps)

            if tuple(map(tuple, child_state.locations)) not in self.seen_states:
                self.seen_states.add(tuple(map(tuple, child_state.locations)))
                self.states.append(child_state)

    def run(self) -> None:
        """
        Runs the algorithm until all possible Board states are visited or a solution
        is found.
        """
        while self.states:

            # get the board instance on top of the stack
            next_state = self.states.pop()

            # stop if we find a solution
            if next_state.check_game_finished():
                break

            self.build_children(next_state)

        self.solution = next_state