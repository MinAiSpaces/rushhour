import os
import time
import argparse

from code.classes import Game
from code.helpers import get_output_path, get_experiment_path
from code.algorithms import StepRefiner
from code.utils import write_moves_to_csv, generate_results
from .random_script import random


def steprefiner(filename: str, game: Game, bin_size: int=10) -> None:
    """
    Executes the Step Refiner algorithm several times for a given game.board,
    writes the search results (number of moves made, solving time) to a CSV file
    in the data/experiment folder, and exports the moves made during the search
    to another CSV file in the data/output folder.
    """
    print(f'Starting Step Refiner for {filename} with {len(game.moves)} steps')
    start_time = time.time()

    n_runs = 0
    results = []

    while time.time() - start_time < 1800:
        start_run_time = time.time()
        steprefiner = StepRefiner(game.board, game.moves, bin_size)
        steprefiner.run()

        if len(steprefiner.new_moves) == len(game.moves):
            if bin_size > 5:
                bin_size -= 1
            else:
                break

        game.moves = steprefiner.new_moves

        n_runs += 1
        if n_runs % 10 == 0:
            print(f'Run: {n_runs} Passed time: {time.time() - start_time}')

        results.append((
            len(steprefiner.new_moves),
            time.time() - start_run_time,
            steprefiner.total_seen_states,
            steprefiner.max_queue_size,
            len(steprefiner.unique_seen_states)
        ))

    print(
        f'Step Refiner used {time.time() - start_time} seconds for '
        f'{n_runs} runs to solve {filename}'
    )

    # get the output and experiment folder paths
    output_path = get_output_path()
    experiment_path = get_experiment_path()
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(experiment_path, exist_ok=True)

    # write the moves made in the last run to the file in the output folder
    export_file_path = os.path.join(output_path, f'StepRefiner_{filename}')
    write_moves_to_csv(export_file_path, steprefiner.new_moves)

    # write the search results to the file in the experiment folder
    experiment_file_path = os.path.join(
        experiment_path, f'StepRefiner_experiment_{filename}'
    )
    generate_results(results, experiment_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='Step Refiner script',
                description='Runs an experiment for 3600 seconds for Step '
                            'Refiner algorithm'
            )

    parser.add_argument(
        'filename',
        help='Filename of the gameboard'
    )
    parser.add_argument(
        '-bz',
        '--bin-size',
        help='Specify the rewind steps (default: 10)'
    )

    args = parser.parse_args()

    filename = args.filename
    game = random(filename, 1800, False)
    bin_size = int(args.bin_size) if args.bin_size else 10

    steprefiner(filename, game, bin_size)
