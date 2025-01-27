import os
import time

from code.classes import Board, Game
from code.helpers import get_output_path, get_experiment_path, get_board_size_from_filename, get_gameboards_path
from code.algorithms import StepRefiner
from code.utils import read_board_state_from_csv, write_moves_to_csv, generate_results


def steprefiner(filename: str, game: Game) -> None:
    """
    Executes the Step Refiner algorithm several times for a given game.board,
    writes the search results (number of moves made, solving time) to a CSV file
    in the data/experiment folder, and exports the moves made during the search
    to another CSV file in the data/output folder.
    """
    print(f'Starting Step Refiner for {filename}')
    start_time = time.time()

    n_runs = 0
    results = []

    while time.time() - start_time < 1800:
        start_run_time = time.time()
        steprefiner = StepRefiner(game.board, game.moves)
        steprefiner.run()

        n_runs += 1
        if n_runs % 10 == 0:
            print(f'Run: {n_runs} Passed time: {time.time() - start_time}')

        results.append((
            len(steprefiner.new_moves),
            time.time() - start_run_time,
            'NaN',
            'NaN'
        ))

    print(f'Step Refiner used {time.time() - start_time} seconds for {n_runs} runs to solve {filename}')

    # get the output and experiment folder paths
    output_path = get_output_path()
    os.makedirs(output_path, exist_ok=True)
    experiment_path = get_experiment_path()
    os.makedirs(experiment_path, exist_ok=True)

    # write the moves made in the last run to the file in the output folder
    export_file_path = os.path.join(output_path, f'StepRefiner_{filename}')
    write_moves_to_csv(export_file_path, steprefiner.new_moves)

    # write the search results to the file in the experiment folder
    experiment_file_path = os.path.join(experiment_path, f'StepRefiner_experiment_{filename}')
    generate_results(results, experiment_file_path)

