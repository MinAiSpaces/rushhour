import csv
import os
import time

from code.classes import Board, Game
from code.helpers import (
    get_input_path,
    get_output_path,
    get_board_size_from_filename
)
from code.algorithms import (
    random_from_all_available_valid,
    DepthFirst,
    BreadthFirst,
    StepRefiner,
    AStar,
    num_blocking_vehicles,
    num_two_blocking_vehicles,
)
from code.scripts import breadth_first
from code.utils import read_board_state_from_csv, write_moves_to_csv


def main():
    filename = 'RushHour6x6_1.csv'
    filename_path = os.path.join(get_input_path(), 'gameboards', filename)
    output_path = get_output_path()
    os.makedirs(output_path, exist_ok=True)

    data = read_board_state_from_csv(filename_path)
    board_size = get_board_size_from_filename(filename)

    board = Game.setup_board(Board(board_size), data)

    # # --------------------------- RandomAllAvailableValid ---------------------
    # start_time = time.time()
    #
    # game = Game(data, board_size)
    # random_from_all_available_valid(game)
    #
    # export_file_path = os.path.join(output_path, f'RandomAllAvailableValid_{filename}')
    # write_moves_to_csv(export_file_path, game.moves)
    #
    # end_time = time.time() - start_time
    # print(end_time)

    # # --------------------------- RandomVehicleFirst --------------------------
    # start_time = time.time()
    #
    # game = Game(data, board_size)
    # random_vehicle_first(game)
    #
    # export_file_path = os.path.join(output_path, f'RandomVehicleFirst_{filename}')
    # write_moves_to_csv(export_file_path, game.moves)
    #
    # end_time = time.time() - start_time
    # print(end_time)

    # # --------------------------- RandomAllAvailableFinish ----------------------
    # start_time = time.time()
    #
    # game = Game(data, board_size)
    # all_available_valid_finish_check(game)
    #
    # export_file_path = os.path.join(output_path, f'RandomAllAvailableFinish_{filename}')
    # write_moves_to_csv(export_file_path, game.moves)
    #
    # end_time = time.time() - start_time
    # print(end_time)

    # # --------------------------- RandomAllMaxMovesFinish ---------------------
    # start_time = time.time()
    #
    # game = Game(data, board_size)
    # all_max_moves_finish_check(game)
    #
    # export_file_path = os.path.join(output_path, f'RandomAllMaxMovesFinish_{filename}')
    # write_moves_to_csv(export_file_path, game.moves)
    #
    # end_time = time.time() - start_time
    # print(end_time)

    # # --------------------------- Depth First ---------------------------------
    # depth = DepthFirst(board)
    #
    # start_time = time.time()
    #
    # depth.run()
    # export_file_path = os.path.join(output_path, f'DepthFirst_{filename}')
    # write_moves_to_csv(export_file_path, depth.moves)
    #
    # end_time = time.time() - start_time
    # print(end_time)

    # # --------------------------- Breadth First --------------------------------
    # breadth = BreadthFirst(board)
    #
    # start_time = time.time()
    #
    # breadth.run()
    # export_file_path = os.path.join(output_path, f'BreadthFirst_{filename}')
    # write_moves_to_csv(export_file_path, breadth.moves)
    #
    # end_time = time.time() - start_time
    # print(end_time)

    # # --------------------------- Step Refiner --------------------------------
    # refiner = StepRefiner(board)

    # print('starting step refiner')
    # start_time = time.time()

    # refiner.run()
    # export_file_path = os.path.join(output_path, f'StepRefiner_{filename}')
    # refiner.board.export_steps(export_file_path)

    # end_time = time.time() - start_time
    # print(f'Step refiner used {end_time} seconds')

    # --------------------------- A-Star ---------------------------------------
    # astar = AStar(board, num_two_blocking_vehicles)
    #
    # start_time = time.time()
    #
    # astar.run()
    # export_file_path = os.path.join(output_path, f'AStar_{filename}')
    # write_moves_to_csv(export_file_path, astar.moves)
    #
    # end_time = time.time() - start_time
    # print(end_time)

    # # ------------------- Script ----------------------------------------------
    # breadth_first('RushHour6x6_2.csv')


if __name__ == '__main__':
    main()
