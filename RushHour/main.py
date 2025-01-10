import csv
import os
from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Board:
    """
    locations = [
         1 2 3 4 5 6
      1 [0,A,A,B,B,B],
      2 [0,C,C,E,D,D],
      3 [X,X,G,E,0,I=,
      4 [F,F,G,H,H,I],
      5 [K,0,L,0,J,J],
      6 [K,0,L,0,0,0],
    ]

    vehicles = {
        'A': Vehicle,
        'B': Vehicle,
        'C': Vehicle,
        'D': Vehicle,
        'E': Vehicle,
        ...
    }
    """
    def __init__(self, size):
        self.size = size
        self.vehicles = {}
        self.steps = []
        self.locations = np.zeros((self.size, self.size), dtype='int')

    def add_vehicle(self, name, vehicle):
        id = len(self.vehicles) + 1 if name != 'X' else -1
        self.vehicles[name] = vehicle

        for i in range(vehicle.length):
            col = vehicle.start_col
            row = vehicle.start_row

            if vehicle.orientation == Orientation.HORIZONTAL:
                self.locations[row, col + i] = id
            else:
                self.locations[row + i, col] = id

    def move_vehicle(self):
        pass

    def plot_board(self):

        available_colors = ['green', 'yellow', 'blue', 'orange', 'purple', 'pink', 'grey', 'brown', 'beige', 'cyan', 'magenta']

        fig, ax = plt.subplots()

        # draw gridlines
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        ax.set_xticks(np.arange(0, self.size + 1, 1));
        ax.set_yticks(np.arange(0, self.size + 1, 1));

        # draw patches
        for idx, vehicle in enumerate(self.vehicles.values()):
            num = idx % len(available_colors)
            color = available_colors[num]
            color = 'red' if vehicle.is_carter else color

            ax.add_patch(Rectangle((vehicle.start_col, vehicle.start_row),
                                    vehicle.length if vehicle.orientation == Orientation.HORIZONTAL else 1,
                                    vehicle.length if vehicle.orientation == Orientation.VERTICAL else 1,
                                    edgecolor = 'black',
                                    facecolor = color,
                                    fill = True,
                                    lw = 1))

        plt.show()

    def export_steps(self, dest_file):
        with open(dest_file, 'w') as f:
            fieldnames = ['car', 'move']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            for step in self.steps:
                writer.writerow({
                    'car': step[0],
                    'move': step[1]
                })


class Vehicle:
    def __init__(self, orientation, start_col, start_row, length, is_carter):
        self.orientation = orientation
        self.start_col = start_col
        self.start_row = start_row
        self.length = length
        self.is_carter = is_carter
        self.location = self.update_location(start_col, start_row)

    def update_location(self, col, row):
        location = []

        for i in range(self.length):
            if self.orientation == Orientation.HORIZONTAL:
                location.append((row, col + i))
            else:
                location.append((row + i, col))

        return location


def get_board_size_from_filename(filename):
    name_first_part = filename.split('_')[0]

    return int(name_first_part.split('x')[1])


def setup_board(board_size, data):
    board = Board(board_size)

    for data_row in data:
        car_name = data_row['car'].upper()
        orientation = data_row['orientation'].upper()
        col = int(data_row['col'])
        row = int(data_row['row'])
        length = int(data_row['length'])

        start_col = col - 1
        start_row = row - 1
        orientation = Orientation.HORIZONTAL if orientation == 'H' else Orientation.VERTICAL
        is_carter = car_name == 'X'

        board.add_vehicle(car_name, Vehicle(orientation, start_col, start_row, length, is_carter))

    return board


def load_board_from_csv(filename_path):
    data = None

    with open(filename_path, 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        data = list(reader)

    return data


def main():
    filename = 'RushHour6x6_1.csv'
    current_dir = os.path.dirname(__file__)
    filename_path = os.path.join(current_dir, '..', 'gameboards', filename)

    data = load_board_from_csv(filename_path)

    board_size = get_board_size_from_filename(filename)

    board = setup_board(board_size, data)

    print(board.locations)
    board.plot_board()

    export_file_path = os.path.join(current_dir, '..', 'output', f'Steps_{filename}')
    board.export_steps(export_file_path)


if __name__ == '__main__':
    main()
