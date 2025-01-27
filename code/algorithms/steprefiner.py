import copy

from code.classes import Board, Mover, Game
from .breadth_first import BreadthFirst


class StepRefiner:
    """
    This class explores the performed moves of a solved board. It does this by saving
    the current board state before reverting the board state back a set number of moves.
    It will then use the Breadth First Search algorithm to find the best route back to
    the previous board state. It will do this repeatedly from the last performed moves
    till the first move while saving the moves from the Breadth First Search algorithm
    as the new solution of the solved board.
    """
    def __init__(self, board: Board, moves: list[tuple[str, int]], bin_size: int=20):
        """
        Initializes StepRefiner with a solved board, using bin_size as the amount of moves
        rewound each iteration. Bins is the amount of iterations necessary to rewind all
        moves excluding a final iteration with last_bin_size amount of moves to rewind.
        """
        if not Game.is_finished(board):
            raise Exception("StepRefiner requires a solved board.")

        self.board = copy.deepcopy(board)
        self.mover = Mover(self.board)
        self.moves = moves

        self.bin_size = bin_size
        self.bins: int = len(self.moves) // self.bin_size
        self.last_bin_size: int = len(self.moves) % self.bin_size

        self.rewind_moves = self.create_rewind_moves()
        self.new_moves: list[tuple[str, int]] = []

    def create_rewind_moves(self) -> list[tuple[str, int]]:
        """
        Returns a list with the opposite moves of the moves in self.moves.
        """
        rewind_moves = []
        for vehicle_name, steps in self.moves:
            rewind_moves.append((vehicle_name, -move))
        return rewind_moves


    def rewind_board(self, moves: int) -> None:
        """
        Rewind the board 'moves' number of moves.
        """
        for i in range(moves):
            move = self.rewind_moves.pop()
            self.mover.move_vehicle(move)

    def run(self) -> None:
        """
        Runs the algorithm rewinding bin_size moves at a time.
        """
        # list[list[tuple[str, int]]]
        new_moves_lists = []

        for bin in range(self.bins):

            # save board state before rewinding
            old_state = copy.deepcopy(self.board.locations)
            self.rewind_board(self.bin_size)

            # find best path back to old_state and save it
            breadth = BreadthFirst(self.board)
            breadth.run(old_state)
            new_moves_lists.append(breadth.moves)

        # check for remaining moves
        if self.last_bin_size > 0:

            # save board state before last rewind
            old_state = copy.deepcopy(self.board.locations)
            self.rewind_board(self.last_bin_size)

            # find best path back to old_state and save it
            breadth = BreadthFirst(self.board)
            breadth.run(old_state)
            new_moves_lists.append(breadth.moves)

        # save moves in correct order
        for list in reversed(new_moves_lists):
            for move in list:
                self.new_moves.append(move)