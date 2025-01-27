import random
from dataclasses import dataclass, field

from code.algorithms import random_from_all_available_valid
from code.classes import (
    Game,
    Board,
    Vehicle,
    BoardPlacementError,
    Orientation,
    BoardPlacementOutOfBoundsError,
    BoardPlacementOccupiedError,
    CARTER_NAME,
    Plotter,
)

@dataclass
class BoardGenerator:
    board_size: int
    board: Board = field(init=False)
    carter: Vehicle = field(init=False)
    vehicle_names: list[str] = field(default_factory=list, init=False)
    orientation_prob: float = field(init=False)
    length_prob: float = field(init=False)

    def __post_init__(self):
        self.vehicle_names = [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'Y',
            'Z',
            'AA',
            'AB',
            'AC',
            'AD',
            'AE',
            'AF',
            'AG',
            'AH',
            'AI',
            'AJ',
            'AK',
            'AL',
            'AM',
            'AN',
            'AO',
            'AP',
            'AQ',
            'AR',
            'AS',
            'AT',
            'AU',
            'AV',
            'AW',
            'AX',
            'AY',
            'AZ',
        ]
        self.orientation_prob = 0.75
        self.length_prob = 0.6
        self.board = Board(self.board_size)

        self._generate_carter()

        self.board.add_vehicle(self.carter)

    def _generate_carter(self) -> None:
        """
        Generates Carter (red car)

        Carter needs to be placed on the board first.
        """
        carter_length = 2

        self.carter = Vehicle(
            CARTER_NAME,
            Orientation.HORIZONTAL,
            random.randint(0, self.board_size - 1 - 3),
            random.randint(0, self.board_size - 1),
            carter_length,
        )

    def _pick_orientation(self):
        """
        Picks an orientation for the next vehicle to be placed.

        If there is only one vehicle (Carter) the next vehicle needs to be
        placed vertically blocking Carter.
        """
        if len(self.board.vehicles) == 1:
            orientation = Orientation.VERTICAL
        else:
            orientation = (
                Orientation.HORIZONTAL
                if random.random() < self.orientation_prob
                else Orientation.VERTICAL
            )

        return orientation

    def _pick_col(self, length: int):
        """
        Picks a column for the next vehicle to be placed.

        If there is only one vehicle (Carter) the next vehicle needs to be
        placed in a column in front of Carter.
        """
        if len(self.board.vehicles) == 1:
            col_carter = self.carter.start_col

            col = random.choice((
                col_carter + self.carter.length,
                col_carter + self.carter.length + 1
            ))
        else:
            col = random.randint(0, self.board_size - 1 - length)

        return col

    def _pick_row(self, col: int, orientation: Orientation, length: int):
        """
        Picks a row for the next vehicle to be placed.

        If there is only one vehicle (Carter) the next vehicle needs to be
        placed in a row so that this vehicle obstructs the path to the exit.

        If a vehicles orientation is Horizontal it can never be placed in front
        of Carter in the same row
        """
        col_carter = self.carter.start_col
        row_carter = self.carter.start_row

        if len(self.board.vehicles) == 1:
            move_up = random.randint(0, length - 1)

            return random.randint(
                row_carter - move_up,
                row_carter,
            )

        if orientation == Orientation.HORIZONTAL:
            row = random.randint(0, self.board_size - 1 - length)

            if col >= col_carter + 2:
                while not row != row_carter:
                    row = random.randint(0, self.board_size - 1 - length)
        else:
            row = random.randint(0, self.board_size - 1 - length)

        return row

    def _generate_vehicle(self) -> Vehicle:
        vehicles_on_board = len(self.board.vehicles)
        name = self.vehicle_names[vehicles_on_board % len(self.vehicle_names)]
        orientation = self._pick_orientation()
        length = 2 if random.random() < self.length_prob else 3
        col = self._pick_col(length)
        row = self._pick_row(col, orientation, length)

        return Vehicle(
            name,
            orientation,
            col,
            row,
            length,
        )

    def add_next_vehicle(self) -> None:
        vehicle = self._generate_vehicle()

        try:
            self.board.add_vehicle(vehicle)
        except BoardPlacementError as exc:
            if isinstance(exc, BoardPlacementOutOfBoundsError):
                print(
                    f"Vehicle '{vehicle.name}' placed out of bounds:",
                    (vehicle.start_col, vehicle.start_row),
                    f'length {vehicle.length}',
                )

            if isinstance(exc, BoardPlacementOccupiedError):
                print(
                    f"Vehicle '{vehicle.name}' placed on top of other:",
                    (vehicle.start_col, vehicle.start_row),
                    f'length {vehicle.length}',
                )


def generate_board(
    board_size: int = 6,
    number_of_vehicles: int = 13,
    iterations: int = 1_000
) -> Board:
    """
    Generates a new board with the correct size.

    It attempts to place as many vehicles as possible until it reaches the
    number_of_vehicles or runs out of allowed iterations.
    """
    generated_board = BoardGenerator(board_size)

    counter = 0
    while (
        len(generated_board.board.vehicles) < number_of_vehicles
        and counter < iterations
    ):
        generated_board.add_next_vehicle()

        counter += 1

    return generated_board.board


def format_board_data(data):
    """
    Helper function to format the generated board's setup data.
    """
    return [
        (
            vehicle[0],
            'H' if vehicle[1] == Orientation.HORIZONTAL else 'V',
            str(vehicle[2]),
            str(vehicle[3]),
            str(vehicle[4]),
        )
        for vehicle in data
    ]


def main():
    plotter = Plotter()
    board_size = 9
    generate_iterations = 20_000

    # 'solve_iterations' was used by a custom random algorithm
    # which limited the number of moves the algorithm was allowed to try before
    # cutting it off. In the current state it will just run until process
    # is interrupted  <ctrl + c>
    # solve_iterations = 50_000

    # Try to generate a board
    board = generate_board(board_size, 26, generate_iterations)

    print('Board generated...')

    # Retrieve the initial setup data of the vehicles on the generated board
    data = []
    for vehicle in board.vehicles.values():
        data.append((
            vehicle.name,
            vehicle.orientation,
            vehicle.start_col,
            vehicle.start_row,
            vehicle.length,
        ))

    # Create a new game with the generated board data
    game = Game(data, board_size)

    # Visually inspect the board.
    # Need to close the plot window before code continues
    plotter.plot_board(game.board)

    print('Checking if board can be solved...')

    random_from_all_available_valid(game)

    # This if-statement is a remnant of the initially used algorithm which
    # would limit the amount of moves the algorithm was allowed to try.
    # There was a high possibility it would not find a solution within the
    # allowed number of moves
    if game.is_finished(game.board):
        print('Board is solved!')

        board_data = format_board_data(data)

        print('moves:', len(game.moves))
        print('vehicles:', len(game.board.vehicles))

        print(board_data)
    else:
        print('Board could not be solved...')


if __name__ == '__main__':
    main()
