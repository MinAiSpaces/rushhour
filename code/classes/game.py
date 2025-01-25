from dataclasses import dataclass, field

from .board import Board
from .mover import Mover
from .plotter import Plotter
from .vehicle import CARTER_NAME, Orientation, Vehicle


class CarterNotOnBoardError(ValueError):
    def __init__(self):
        super().__init__('Carter appears to not be on the board')


@dataclass
class Game:
    """
    Game is responsible for managing the overall gameplay and flow.
    It acts as the central interface for interacting with the game, handling
    board setup, move execution through the Mover, move history tracking
    and checking if the game is finished. The Game class also allows for easy
    visualizing of the current state of the board through the Plotter.
    """
    data: list[tuple[str, Orientation, int, int, int]]
    board_size: int
    board: Board = field(init=False)
    mover: Mover = field(init=False)
    plotter: Plotter = field(init=False)
    moves: list[tuple[str, int]] = field(default_factory=list, init=False)

    def __post_init__(self):
        """
        The initialization of the Game creates an empty board of size
        'board_size'.

        Next we place all the vehicles on the board and encapsulate the Mover
        and Plotter.
        """
        self.board = self.setup_board(Board(self.board_size), self.data)
        self.mover = Mover(self.board)
        self.plotter = Plotter()

    def get_all_available_moves(
        self,
        vehicle_name: str | None = None
    ) -> list[tuple[str, int]]:
        """
        Gets all available valid moves at the current game state.
        """
        return self.mover.get_all_available_moves(vehicle_name)

    def make_move(self, move: tuple[str, int]) -> None:
        """
        Plays a move and appends it to the moves history.
        """
        self.mover.move_vehicle(move)
        self.moves.append(move)

    def is_finished(self) -> bool:
        """
        Checks if Carter (the red car) has reach the right side of the board.

        Checks if the front of Carter occupies the last column on the right.
        """
        carter = self.board.vehicles.get(CARTER_NAME)

        if carter is None:
            raise CarterNotOnBoardError()

        col_carter_front = carter.location[-1][0]

        return col_carter_front == self.board.size - 1

    def plot_board(self, file_path: str | None = None) -> None:
        """
        Plots the current state of the board using the Plotter.

        if 'file_path' is provided it will try to export the image to the
        provided path.
        """
        self.plotter.plot_board(self.board, file_path)

    @staticmethod
    def setup_board(
        board: Board,
        data: list[tuple[str, Orientation, int, int, int]]
    ) -> Board:
        """
        Setup function to place vehicles on provided board in order to create
        a new board or restore an old board.

        This function is static so that it can also be used to set up a board
        without using the rest of the Game class.
        """
        for vehicle_data in data:
            board.add_vehicle(
                Vehicle(*vehicle_data)
            )

        return board


