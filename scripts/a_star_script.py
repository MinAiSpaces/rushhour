import os
import time
import argparse

from code.classes import Board, Game
from code.helpers import get_output_path, get_experiment_path, get_board_size_from_file_path, get_gameboards_path
from code.algorithms import AStar, num_blocking_vehicles
from code.utils import read_board_state_from_csv, write_moves_to_csv, generate_results


def a_star(filename: str, max_moves: bool=True) -> None:
    """
    Executes the A-Star algorithm several times for a given Board, writes
    the search results (number of moves made, solving time, number of seen states, max
    size of queue) to a CSV file in the data/experiment folder, and exports the moves
    made during the search to another CSV file in the data/output folder.
    """
    print(max_moves)
    filename_path = os.path.join(get_gameboards_path(), filename)

    board_size = get_board_size_from_file_path(filename)
    data = read_board_state_from_csv(filename_path)
    board = Game.setup_board(Board(board_size), data)

    print(f'Starting A-Star for {filename}')
    start_time = time.time()

    n_runs = 0
    results = []

    while time.time() - start_time < 3600:
        start_run_time = time.time()
        astar = AStar(board, num_blocking_vehicles)
        astar.run(max_moves)

        n_runs += 1
        if n_runs % 10 == 0:
            print(f'Run: {n_runs} Passed time: {time.time() - start_time}')

        results.append((
            len(astar.moves),
            time.time() - start_run_time,
            len(astar.seen_states),
            astar.max_queue_size,
            len(astar.seen_states)
        ))

    print(f'A-Star used {time.time() - start_time} seconds for {n_runs} runs to solve {filename}')

    # get the output and experiment folder paths
    output_path = get_output_path()
    os.makedirs(output_path, exist_ok=True)
    experiment_path = get_experiment_path()
    os.makedirs(experiment_path, exist_ok=True)

    # write the moves made in the last run to the file in the output folder
    export_file_path = os.path.join(output_path, f'AStar_{filename}')
    write_moves_to_csv(export_file_path, astar.moves)

    # write the search results to the file in the experiment folder
    experiment_file_path = os.path.join(experiment_path, f'AStar_experiment_{filename}')
    generate_results(results, experiment_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='A-Star script',
                description='Runs an experiment for 3600 seconds for A-Star'
            )

    parser.add_argument('filename', help='Filename of the gameboard')
    parser.add_argument('-nmm', '--no-max-moves', action='store_false', help='Boolean flag to disable max moves')

    args = parser.parse_args()

    filename = args.filename
    no_max_moves = args.no_max_moves

    a_star(filename, no_max_moves)
