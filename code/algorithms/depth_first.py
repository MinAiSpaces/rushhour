import copy

from code.classes import Board, Mover, Game


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
        self.states = [(copy.deepcopy(initial_state), [])]
        self.seen_states: set[tuple[tuple[object]]] = set()
        self.solution = None
        self.moves: list[tuple[str, int]] = []

    def build_children(self, next_state: Board, move_history: list[tuple[str, int]]) -> None:
        """
        Generates all possible child states from the picked Board state and appends
        them to the stack of states if not seen earlier. Each child state represents
        the Board configuration after a valid move by a Vehicle.
        """
        mover = Mover(next_state)
        possible_moves: list[tuple[str, int]] = mover.get_all_available_moves()

        # add a new board instance to the stack for each valid move
        for move in possible_moves:
            child_state = copy.deepcopy(next_state)
            new_mover = Mover(child_state)

            # make the valid move in the new board instance
            new_mover.move_vehicle(move)

            # https://www.geeksforgeeks.org/how-to-fix-the-typeerror-unhashable-type-numpy-ndarray/
            if tuple(map(tuple, child_state.locations)) not in self.seen_states:
                self.seen_states.add(tuple(map(tuple, child_state.locations)))
                self.states.append((child_state, move_history + [move]))

    def run(self) -> None:
        """
        Runs the algorithm until all possible Board states are visited or a solution
        is found.
        """
        while self.states:

            # get the board instance on top of the stack
            next_state, move_history = self.states.pop()

            # stop if we find a solution
            if Game.is_finished(next_state):
                self.solution = next_state
                self.moves = move_history
                break

            self.build_children(next_state, move_history)

        self.solution = next_state
