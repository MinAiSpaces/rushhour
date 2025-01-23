import concurrent.futures
import csv
import os
import statistics
import time
import copy

import matplotlib.pyplot as plt
import numpy as np

from code.algorithms import all_available_valid_finish_check, all_max_moves_finish_check, StepRefiner
from code.classes import Board, Vehicle, Orientation
from code.helpers import get_input_path, get_output_path, get_board_size_from_filename


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


def create_plots(steps: list[int], filename: str,  bins: int = 25) -> None:
    fig, axs = plt.subplots(1, 2, tight_layout=True)

    axs[0].hist(steps, bins=bins)
    axs[0].set_title('Distribution of steps')
    axs[0].set_xlabel('Number of steps')
    axs[0].set_ylabel('Count')

    axs[1].bar(np.arange(1, len(steps)+1), steps)
    axs[1].set_title('Sorted steps per game')
    axs[1].set_xlabel('Sorted game index')
    axs[1].set_ylabel('Number of steps')

    #check_or_create_dir(os.path.join(get_output_path(), 'images'))
    #fname = os.path.join(get_output_path(), 'images', filename)

    #plt.savefig(fname=fname, dpi=300)

    plt.show()


def main():
    filename = 'RushHour6x6_1.csv'
    filename_path = os.path.join(get_input_path(), 'gameboards', filename)
    output_path = get_output_path()
    os.makedirs(output_path, exist_ok=True)
    export_file_path = os.path.join(output_path, f'Steps_{filename}')

    data = load_board_from_csv(filename_path)

    board = setup_board(get_board_size_from_filename(filename), data)

    print(board.locations)
    all_max_moves_finish_check(board)
    print(board.locations)
    step_refiner = StepRefiner(board)
    step_refiner.rewind_board(len(board.steps))
    print(step_refiner.board.locations)


    # steps = []
    # for i in range(1000):
    #     if i % 50 == 0:
    #         print(i)
    #     game_board = copy.deepcopy(board)
    #     all_available_valid_finish_check(game_board)
    #     steps.append(len(game_board.steps))


    # cpu_count = os.cpu_count()
    # max_workers = cpu_count * 3

    # playing_boards = {}
    # steps = []
    # iterations = 10_000
    # start = time.time()

    # with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
    #     for i in range(iterations):
    #         print(f'Adding task {i} to pool')
    #         game_board = copy.deepcopy(board)
    #         playing_boards[executor.submit(all_available_valid_finish_check, game_board)] = i

    #     print(f'Tasks running...')

    #     for future in concurrent.futures.as_completed(playing_boards):
    #         try:
    #             solved_board = future.result()
    #             num_steps = len(solved_board.steps)
    #             steps.append(num_steps)

    #             if (len(steps) % 100) == 0:
    #                 print(f'Successfully solved {len(steps)} boards')
    #         except Exception as exc:
    #             print('Encountered error in solving boards concurrently')

    # elapsed = time.time() - start

    # steps.sort()

    # print(len(steps))
    # print(f'Ran {iterations} iterations in {elapsed} seconds')
    # print('Least amount of steps:', steps[0])
    # print('Most steps:', steps[-1])
    # print('Average number of steps:', statistics.mean(steps))
    # print('Median:', statistics.median(steps))
    # print('Mode:', statistics.mode(steps))
    # print('Std:', statistics.stdev(steps))
    # print('Qrts:', statistics.quantiles(steps))

    # create_plots(steps, f"{filename.split('.')[0]}_baseline.png", 50)


if __name__ == '__main__':
    main()
