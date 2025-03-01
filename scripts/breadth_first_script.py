import os
import time
import argparse

from code.classes import Board, Game
from code.helpers import (
    get_output_path,
    get_experiment_path,
    get_board_size_from_file_path,
    get_gameboards_path,
)
from code.algorithms import BreadthFirst
from code.utils import (
    read_board_state_from_csv,
    write_moves_to_csv,
    generate_results,
)


def breadth_first(
    filename: str,
    max_moves: bool = True,
    useful_move: bool = False,
) -> None:
    """
    Executes the Breadth First Search algorithm several times for a given Board, writes
    the search results (number of moves made, solving time, number of seen states, max
    size of queue) to a CSV file in the data/experiment folder, and exports the moves
    made during the search to another CSV file in the data/output folder.
    """
    filename_path = os.path.join(get_gameboards_path(), filename)

    board_size = get_board_size_from_file_path(filename)
    data = read_board_state_from_csv(filename_path)
    board = Game.setup_board(Board(board_size), data)

    print(f'Starting Breadth First for {filename}')
    start_time = time.time()

    n_runs = 0
    results = []

    while time.time() - start_time < 3600:
        start_run_time = time.time()
        breadth = BreadthFirst(board)
        breadth.run(max_moves=max_moves, useful_move=useful_move)

        n_runs += 1
        if n_runs % 10 == 0:
            print(f'Run: {n_runs} Passed time: {time.time() - start_time}')

        results.append((
            len(breadth.moves),
            time.time() - start_run_time,
            len(breadth.seen_states),
            breadth.max_queue_size,
            len(breadth.seen_states)
        ))

    print(
        f'Breadth First used {time.time() - start_time} seconds '
        f'for {n_runs} runs to solve {filename}'
    )

    # get the output and experiment folder paths
    output_path = get_output_path()
    experiment_path = get_experiment_path()
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(experiment_path, exist_ok=True)

    # write the moves made in the last run to the file in the output folder
    export_file_path = os.path.join(output_path, f'BreadthFirst_{filename}')
    write_moves_to_csv(export_file_path, breadth.moves)

    # write the search results to the file in the experiment folder
    experiment_file_path = os.path.join(
        experiment_path, f'BreadthFirst_experiment_{filename}'
    )
    generate_results(results, experiment_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='Breadth First script',
                description='Runs an experiment for 3600 seconds for Breadth '
                            'First algorithm'
            )

    parser.add_argument(
        'filename',
        help='Filename of the gameboard',
    )
    parser.add_argument(
        '-nmm',
        '--no-max-moves',
        action='store_false',
        help='Boolean flag to disable max moves',
    )
    parser.add_argument(
        '-um',
        '--useful-move',
        action='store_true',
        help='Boolean flag to enable only useful moves',
    )

    args = parser.parse_args()

    filename = args.filename
    no_max_moves = args.no_max_moves
    useful_move = args.useful_move

    breadth_first(filename, no_max_moves, useful_move)
