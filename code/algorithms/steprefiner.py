import copy

import numpy as np

from code.classes import Vehicle, Board


class StepRefiner:
    def __init__(self, board: Board, bins: int=10)
        if not board.check_game_finished():
            raise Exception("StepRefiner requires a solved board.")

        self.board = copy.deepcopy(board)
        self.bins = bins
        self.rewind_steps = self.create_rewind_steps()

    def create_rewind_steps(self) -> list[tuple[Vehicle, int]]:
        """
        Returns a list with the exact opposite steps of the steps in self.board.steps.
        """
        rewind_steps = []
        for vehicle, move in self.board.steps:
            rewind_steps.append((vehicle, -move))
        return rewind_steps


    def rewind_board(self, steps: int) -> Board:
        """
        Rewind the board 'steps' number of moves
        """
        for i in range(steps):
            step = self.rewind_steps.pop()
            self.board.move_vehicle(step[0], step[1])

