import csv
import os

from classes import orientation as orient
from classes import board as game_board
from classes import vehicle


def get_board_size_from_filename(filename):
    name_first_part = filename.split('_')[0]

    return int(name_first_part.split('x')[1])


def setup_board(board_size, data):
    board = game_board.Board(board_size)

    for data_row in data:
        car_name = data_row['car'].upper()
        orientation = data_row['orientation'].upper()
        col = int(data_row['col'])
        row = int(data_row['row'])
        length = int(data_row['length'])

        start_col = col - 1
        start_row = row - 1
        orientation = orient.Orientation.HORIZONTAL if orientation == 'H' else orient.Orientation.VERTICAL

        board.add_vehicle(vehicle.Vehicle(car_name, orientation, start_col, start_row, length))

    return board


def load_board_from_csv(filename_path):
    data = None

    with open(filename_path, 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        data = list(reader)

    return data


def main():
    filename = 'RushHour6x6_test.csv'
    current_dir = os.path.dirname(__file__)
    filename_path = os.path.join(current_dir, '..', 'tests', 'gameboards', filename)

    data = load_board_from_csv(filename_path)

    board_size = get_board_size_from_filename(filename)

    board = setup_board(board_size, data)

    print(board.locations)
    board.plot_board()

    export_file_path = os.path.join(current_dir, '..', 'output', f'Steps_{filename}')
    board.export_steps(export_file_path)

    vehicle_x = board.vehicles['X']
    vehicle_a = board.vehicles['A']
    vehicle_b = board.vehicles['B']

    print(vehicle_b.location)
    print(board.check_move_forwards(vehicle_b))
    board.move_vehicle(vehicle_b, 2)
    print(board.check_move_backwards(vehicle_b))

    print(vehicle_a.location)
    board.move_vehicle(vehicle_a, 3)
    board.move_vehicle(vehicle_a, -1)
    print(vehicle_a.location)

    print(board.steps)
    board.plot_board()
    board.export_steps(export_file_path)


if __name__ == '__main__':
    main()
