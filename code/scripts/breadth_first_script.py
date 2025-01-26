import csv
import os
import time

from code.classes import Board, Game
from code.helpers import get_output_path, get_experiment_path, get_board_size_from_filename, get_gameboards_path
from code.algorithms import BreadthFirst
from code.utils import read_board_state_from_csv, write_moves_to_csv


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
    filename_path = os.path.join(get_gameboards_path(), filename)

    # get the output and experiment folder paths
    output_path = get_output_path()
    os.makedirs(output_path, exist_ok=True)
    experiment_path = get_experiment_path()
    os.makedirs(experiment_path, exist_ok=True)

    board_size = get_board_size_from_filename(filename)
    data = read_board_state_from_csv(filename_path)
    board = Game.setup_board(Board(board_size), data)

    print(f'Starting Breadth First for {filename}')
    start_time = time.time()

    breadth = BreadthFirst(board)
    breadth.run()

    # write the moves made to the file in the output folder
    export_file_path = os.path.join(output_path, f'BreadthFirst_{filename}')
    write_moves_to_csv(export_file_path, breadth.moves)

    # write the num moves made and solving time to the file in the experiment folder
    experiment_file_path = os.path.join(experiment_path, f'BreadthFirst_experiment_{filename}')
    num_moves_made = len(breadth.moves)
    solving_time = time.time() - start_time
    generate_results(num_moves_made, solving_time, experiment_file_path)

    print(f'Breadth First used {solving_time} seconds to solve {filename}')