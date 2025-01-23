import copy

import numpy as np

from code.classes import Vehicle, Board


class StepRefiner:
    def __init__(self, board: Board, bin_size: int=20):
        if not board.check_game_finished():
            raise Exception("StepRefiner requires a solved board.")

        self.board = copy.deepcopy(board)
        self.bin_size = bin_size
        self.bins = len(self.board.steps) // self.bin_size
        self.last_bin_size = len(self.board.steps) % self.bin_size

        self.rewind_steps = self.create_rewind_steps()

    def create_rewind_steps(self) -> list[tuple[str, int]]:
        """
        Returns a list with the exact opposite steps of the steps in self.board.steps.
        """
        rewind_steps = []
        for vehicle_name, move in self.board.steps:
            rewind_steps.append((vehicle_name, -move))
        return rewind_steps


    def rewind_board(self, steps: int) -> None:
        """
        Rewind the board 'steps' number of moves
        """
        for i in range(steps):
            step = self.rewind_steps.pop()
            self.board.move_vehicle(self.board.vehicles[step[0]], step[1])

    def run(self) -> Board:
        """
        Runs the StepRefiner.
        """
        new_steps = []

        for bin in range(self.bins):
            self.board.steps = []
            old_state = self.board.locations
            self.rewind_board(self.bin_size)
            # BreadthFirst
            # save steps (think of order)

        self.board.steps = []
        old_state = self.board.locations
        self.rewind_board(self.last_bin_size)
        # BreadthFirst
        # save steps (think of order)