from .depth_first import DepthFirst


class BreadthFirst(DepthFirst):
    """
    This class explores all possible Board configurations by performing a Breadth First
    Search algorithm, starting from an initial Board state. It maintains a queue of
    Board states, generates child states for valid moves, and continues the search
    until a solution is found.

    Uses DepthFirst as the parent class, because the only difference is the usage of
    a queue instead of a stack.
    """

    def get_next_state(self):
        """
        Gets the next state from the list of states.
        """
        return self.states.pop(0)