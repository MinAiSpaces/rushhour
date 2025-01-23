import copy

import numpy as np

from code.classes import Vehicle, Board
from .breadth_first import BreadthFirst


class StepRefiner:
    """
    This class explores the performed steps of a solved board. It does this by saving
    the current board state before reverting the board state back a set number of steps.
    It will then use the Breadth First Search algorithm to find the best route back to
    the previous board state. It will do this repeatedly from the last performed steps
    till the first step while saving the steps from the Breadth First Search algorithm
    as the new solution of the solved board.
    """
    def __init__(self, board: Board, bin_size: int=20):
        """
        Initializes StepRefiner with a solved board, using bin_size as the amount of steps
        rewound each iteration. Bins is the amount of iterations necessary to rewind all
        steps excluding a final iteration with last_bin_size amount of steps to rewind.
        """
        if not board.check_game_finished():
            raise Exception("StepRefiner requires a solved board.")

        self.board = copy.deepcopy(board)
        self.bin_size = bin_size
        self.bins: int = len(self.board.steps) // self.bin_size
        self.last_bin_size: int = len(self.board.steps) % self.bin_size

        self.rewind_steps = self.create_rewind_steps()

    def create_rewind_steps(self) -> list[tuple[str, int]]:
        """
        Returns a list with the opposite steps of the steps in self.board.steps.
        """
        rewind_steps = []
        for vehicle_name, move in self.board.steps:
            rewind_steps.append((vehicle_name, -move))
        return rewind_steps


    def rewind_board(self, steps: int) -> None:
        """
        Rewind the board 'steps' number of moves.
        """
        for i in range(steps):
            step = self.rewind_steps.pop()
            self.board.move_vehicle(self.board.vehicles[step[0]], step[1])

    def run(self) -> Board:
        """
        Runs the algorithm rewinding bin_size steps at a time.
        """
        # list[list[tuple[str, int]]]
        all_new_steps = []
        #list[tuple[str, int]]
        new_steps = []

        for bin in range(self.bins):

            # save board state before further rewinding
            old_state = copy.deepcopy(self.board.locations)
            self.rewind_board(self.bin_size)

            # reset steps
            self.board.steps = []

            # find best path back to old_state and save it
            breadth = BreadthFirst(self.board)
            breadth.run(old_state)
            all_new_steps.append(breadth.solution.steps)

        # save board state before further rewinding
        old_state = copy.deepcopy(self.board.locations)
        self.rewind_board(self.last_bin_size)

        # reset steps
        self.board.steps = []

        # find best path back to old_state and save it
        breadth = BreadthFirst(self.board)
        breadth.run(old_state)
        all_new_steps.append(breadth.solution.steps)

        # save steps in correct order
        for list in reversed(all_new_steps):
            for step in list:
                new_steps.append(step)

        self.board.steps = new_steps