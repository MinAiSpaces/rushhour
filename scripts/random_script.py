import os
import time
import argparse

from code.classes import Game
from code.helpers import (
    get_output_path,
    get_experiment_path,
    get_board_size_from_file_path,
    get_gameboards_path,
)
from code.algorithms import all_max_moves_finish_check
from code.utils import (
    read_board_state_from_csv,
    write_moves_to_csv,
    generate_results,
)


def random(
    filename: str,
    set_time: int = 3600,
    write_results: bool = True
) -> Game:
    """
    Executes the Random algorithm several times for a given Board, writes
    the search results (number of moves made, solving time) to a CSV file in
    the data/experiment folder, exports the moves made during the search
    to another CSV file in the data/output folder, and returns the Board from
    a run with the least number of moves made.
    """
    filename_path = os.path.join(get_gameboards_path(), filename)

    board_size = get_board_size_from_file_path(filename)
    data = read_board_state_from_csv(filename_path)

    print(f'Starting Random for {filename}')
    start_time = time.time()

    n_runs = 0
    results = []
    best_solution = ('game', float('inf'))

    while time.time() - start_time < set_time:
        start_run_time = time.time()
        game = Game(data, board_size)
        all_max_moves_finish_check(game)

        n_runs += 1
        if n_runs % 10 == 0:
            print(f'Run: {n_runs} Passed time: {time.time() - start_time}')

        results.append((
            len(game.moves),
            time.time() - start_run_time,
            len(game.moves),
            'NaN',
            'NaN'
        ))

        # save the run with the least num of moves
        if len(game.moves) < best_solution[1]:
            best_solution = (game, len(game.moves))

    print(
        f'Random used {time.time() - start_time} seconds for '
        f'{n_runs} runs to solve {filename}'
    )

    if write_results:
        # get the output and experiment folder paths
        output_path = get_output_path()
        experiment_path = get_experiment_path()
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(experiment_path, exist_ok=True)

        # write the moves made in the best run to the file in the output folder
        export_file_path = os.path.join(output_path, f'Random_{filename}')
        write_moves_to_csv(export_file_path, best_solution[0].moves)

        # write the search results to the file in the experiment folder
        experiment_file_path = os.path.join(
            experiment_path, f'Random_experiment_{filename}'
        )
        generate_results(results, experiment_file_path)

    return best_solution[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='Randomise script',
                description='Runs an experiment for 3600 seconds for '
                            'Randomise algorithm'
            )

    parser.add_argument(
        'filename',
        help='Filename of the gameboard'
    )

    args = parser.parse_args()

    filename = args.filename

    random(filename)
