from dataclasses import dataclass, field

from .board import Board
from .mover import Mover, MoveError
from .plotter import Plotter
from .vehicle import CARTER_NAME, Orientation, Vehicle


class GameError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)


class SetupBoardNoCarterError(GameError):
    def __init__(self):
        super().__init__('Carter appears to be missing on the board')


class SetupBoardNoVehicleDataError(GameError):
    def __init__(self):
        super().__init__('No vehicle data provided')


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

    def plot_board(self, file_path: str | None = None, dpi: int = 300) -> None:
        """
        Plots the current state of the board using the Plotter.

        if 'file_path' is provided it will try to export the image to the
        provided path.
        """
        self.plotter.plot_board(self.board, file_path, dpi)

    def animate_moves(
        self,
        moves: list[tuple[str, int]] | None = None,
        interval: int = 500,
        file_path: str | None = None,
        writer_type: str = 'pillow',
        verbose: bool = True,
    ):
        """
        Animates the moves.

        The writer_type is used for saving the animation ('pillow', 'ffmpeg').
            - Use Pillow to generate gifs
            - Use ffmpeg to generate mp4 (videos)

        NB.
        Replays all moves using the Game class so board needs to be in
        correct 'start state' or we'll run into move conflicts.
        """
        if moves is None:
            moves = self.moves

        self.plotter.animate_moves(
            self,
            moves,
            interval,
            file_path,
            writer_type,
            verbose,
        )

    def reset(self):
        """
        Resets the game to its original starting state.

        NB.
        Removes any moves stored in the current game instance
        """
        original_data = [
            (
                vehicle.name,
                vehicle.orientation,
                vehicle.start_col,
                vehicle.start_row,
                vehicle.length
            )
            for vehicle in self.board.vehicles.values()
        ]

        self.board = self.setup_board(Board(self.board.size), original_data)
        self.mover = Mover(self.board)
        self.moves.clear()

    def is_valid_solution(self, moves_file_path: str) -> bool:
        """
        Checks if the moves in the provided file lead to a valid solution

        NB.
        Replays all moves using the Game class so board needs to be in
        correct 'start state' or we'll run into move conflicts.
        """
        from code.utils import read_moves_from_csv

        moves = read_moves_from_csv(moves_file_path)

        for move in moves:
            try:
                self.make_move(move)
            except MoveError:
                return False

        return self.is_finished(self.board)

    def write_moves_to_csv(self, file_path: str) -> None:
        """
        Write moves to a CSV file.

        Writes a header row consisting of the fieldnames
        And a row for every move containing:
            - the vehicle name
            - the steps (positive for forwards, negative for backwards)
        """
        from code.utils import write_moves_to_csv

        write_moves_to_csv(file_path, self.moves)

    def write_board_state_to_csv(self, file_path: str) -> None:
        """
        Write current board state to a CSV file.
        """
        from code.utils import write_board_state_to_csv

        write_board_state_to_csv(file_path, list(self.board.vehicles.values()))

    @classmethod
    def load_board_state_from_csv(cls, board_file_path: str) -> 'Game':
        """
        Creates a new Game from board data from csv file.
        """
        from code.helpers import get_board_size_from_file_path
        from code.utils import read_board_state_from_csv

        board_size = get_board_size_from_file_path(board_file_path)
        data = read_board_state_from_csv(board_file_path)

        return cls(data, board_size)

    @staticmethod
    def is_finished(board: Board) -> bool:
        """
        Checks if Carter (the red car) has reach the right side of the board.

        Checks if the front of Carter occupies the last column on the right.
        """
        carter = board.vehicles[CARTER_NAME]
        col_carter_front = carter.location[-1][0]

        return col_carter_front == board.size - 1

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
        if not len(data):
            raise SetupBoardNoVehicleDataError()

        for vehicle_data in data:
            board.add_vehicle(
                Vehicle(*vehicle_data)
            )

        if board.vehicles.get(CARTER_NAME) is None:
            raise SetupBoardNoCarterError()

        return board

