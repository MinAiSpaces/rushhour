import csv
import os
import time

from code.classes import Board, Vehicle, Orientation
from code.helpers import get_input_path, get_output_path, get_board_size_from_filename

from code.algorithms import random_from_all_available_valid
from code.algorithms import DepthFirst
from code.algorithms import BreadthFirst
from code.algorithms import StepRefiner


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


def main():
    filename = 'RushHour9x9_4.csv'
    filename_path = os.path.join(get_input_path(), 'gameboards', filename)
    output_path = get_output_path()
    os.makedirs(output_path, exist_ok=True)

    data = load_board_from_csv(filename_path)

    board = setup_board(get_board_size_from_filename(filename), data)

    # --------------------------- Random ---------------------------------------
    # random_from_all_available_valid(board)

    # board.export_steps(export_file_path)

    # --------------------------- Depth First ----------------------------------
    depth = DepthFirst(board)

    start_time = time.time()

    depth.run()
    export_file_path = os.path.join(output_path, f'DepthFirst_{filename}')
    depth.solution.export_steps(export_file_path)

    end_time = time.time() - start_time
    print(end_time)

    # --------------------------- Breadth First --------------------------------
    breadth = BreadthFirst(board)

    start_time = time.time()

    breadth.run()
    export_file_path = os.path.join(output_path, f'BreadthFirst_{filename}')
    breadth.solution.export_steps(export_file_path)

    end_time = time.time() - start_time
    print(end_time)

if __name__ == '__main__':
    main()
