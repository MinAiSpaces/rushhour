import csv
import os
import time

from code.classes import Board, Vehicle, Orientation
from code.helpers import get_input_path, get_output_path, get_experiment_path, get_board_size_from_filename
from code.algorithms import BreadthFirst


def setup_board(board_size: int, data: list[dict[str, str | int]]) -> Board:
    """
    Initialize a new board and add all vehicles from data to the board.
    """
    board = Board(board_size)

    # get all parameters for the vehicles
    for data_row in data:
        car_name = data_row['car'].upper()
        orientation = data_row['orientation'].upper()
        col = int(data_row['col'])
        row = int(data_row['row'])
        length = int(data_row['length'])

        # change col and row to be from 0 to 5 instead of 1 to 6 for easier plotting
        start_col = col - 1
        start_row = row - 1
        orientation = Orientation.HORIZONTAL if orientation == 'H' else Orientation.VERTICAL

        board.add_vehicle(Vehicle(car_name, orientation, start_col, start_row, length))

    return board


def load_board_from_csv(filename_path: str) -> list[dict[str, str | int]]:
    """
    Read csv file and return a list of dictionaries.
    Every dictionary represents 1 vehicle.
    """
    data = None

    with open(filename_path, 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        data = list(reader)

    return data


def generate_results(num_moves_made: int, solving_time: float, dest_file: str) -> None:
    """
    Writes all the search results (solving time, number of moves made) to a
    CSV file.
    """
    with open(dest_file, 'w', newline='') as f:
        fieldnames = ['number moves made', 'solving time']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'number moves made': num_moves_made, 'solving time': solving_time})


def breadth_first(filename: str) -> None:
    """
    Executes the Breadth First Search algorithm for a given Board, writes the
    search results (solving time, number of moves made) to a CSV file in the
    data/experiment folder, and exports the moves made during the search to
    another CSV file in the data/output folder.
    """
    filename_path = os.path.join(get_input_path(), 'gameboards', filename)

    # get the output and experiment folder paths
    output_path = get_output_path()
    os.makedirs(output_path, exist_ok=True)
    experiment_path = get_experiment_path()
    os.makedirs(experiment_path, exist_ok=True)

    data = load_board_from_csv(filename_path)
    board = setup_board(get_board_size_from_filename(filename), data)

    print(f'Starting Breadth First for {filename}')
    start_time = time.time()

    breadth = BreadthFirst(board)
    breadth.run()

    # write the moves made to the file in the output folder
    export_file_path = os.path.join(output_path, f'BreadthFirst_{filename}')
    breadth.solution.export_steps(export_file_path)

    # write the num moves made and solving time to the file in the experiment folder
    experiment_file_path = os.path.join(experiment_path, f'BreadthFirst_experiment_{filename}')
    num_moves_made = len(breadth.solution.steps)
    solving_time = time.time() - start_time
    generate_results(num_moves_made, solving_time, experiment_file_path)

    print(f'Breadth First used {solving_time} seconds to solve {filename}')