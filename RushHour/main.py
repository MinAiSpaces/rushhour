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
        self.locations = np.zeros((self.size, self.size), dtype='object')

    def add_vehicle(self, vehicle):
        name = vehicle.name
        self.vehicles[name] = vehicle

        coords = vehicle.location
        self.update_locations(coords, name)

    def update_locations(self, coords, value):
        for i in range(len(coords)):
            row, col = coords[i]

            self.locations[row, col] = value

    def check_move_forwards(self, vehicle):
        board_boundary = self.size - 1
        orientation = vehicle.orientation
        row_vehicle_front, col_vehicle_front = vehicle.location[-1]

        if orientation == Orientation.HORIZONTAL:
            possible_steps = board_boundary - col_vehicle_front

            for step in range(1, possible_steps + 1):
                if self.locations[row_vehicle_front, col_vehicle_front + step] != 0:
                    return step - 1
        else:
            possible_steps = board_boundary - row_vehicle_front

            for step in range(1, possible_steps + 1):
                if self.locations[row_vehicle_front + step, col_vehicle_front] != 0:
                    return step - 1

        return possible_steps

    def check_move_backwards(self, vehicle):
        orientation = vehicle.orientation
        row_vehicle_back, col_vehicle_back = vehicle.location[0]

        if orientation == Orientation.HORIZONTAL:
            possible_steps = col_vehicle_back

            for step in range(1, possible_steps + 1):
                if self.locations[row_vehicle_back, col_vehicle_back - step] != 0:
                    return step - 1
        else:
            possible_steps = row_vehicle_back

            for step in range(1, possible_steps + 1):
                if self.locations[row_vehicle_back - step, col_vehicle_back] != 0:
                    return step - 1

        return possible_steps

    def move_vehicle(self, vehicle, steps):
        if steps == 0:
            raise ValueError

        if steps > 0:
            if steps > self.check_move_forwards(vehicle):
                raise ValueError
        else:
            if -steps > self.check_move_backwards(vehicle):
                raise ValueError

        old_coords = vehicle.location
        row_vehicle_back, col_vehicle_back = old_coords[0]

        if steps > 0:
            if vehicle.orientation == Orientation.HORIZONTAL:
                vehicle.update_location(col_vehicle_back + steps, row_vehicle_back)
            else:
                vehicle.update_location(col_vehicle_back, row_vehicle_back + steps)
        else:
            if vehicle.orientation == Orientation.HORIZONTAL:
                vehicle.update_location(col_vehicle_back + steps, row_vehicle_back)
            else:
                vehicle.update_location(col_vehicle_back, row_vehicle_back + steps)

        self.steps.append((vehicle.name, steps))

        self.update_locations(old_coords, 0)
        self.update_locations(vehicle.location, vehicle.name)

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

            ax.add_patch(Rectangle((vehicle.location[0][1], vehicle.location[0][0]),
                                    vehicle.length if vehicle.orientation == Orientation.HORIZONTAL else 1,
                                    vehicle.length if vehicle.orientation == Orientation.VERTICAL else 1,
                                    edgecolor = 'black',
                                    facecolor = color,
                                    fill = True,
                                    lw = 1))

        plt.show()

    def export_steps(self, dest_file):
        with open(dest_file, 'w', newline='') as f:
            fieldnames = ['car', 'move']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            for step in self.steps:
                writer.writerow({
                    'car': step[0],
                    'move': step[1]
                })


class Vehicle:
    def __init__(self, name, orientation, start_col, start_row, length):
        self.name = name
        self.orientation = orientation
        self.start_col = start_col
        self.start_row = start_row
        self.length = length
        self.is_carter = name == 'X'
        self.location = []

        self.update_location(start_col, start_row)

    def update_location(self, col, row):
        location = []

        for i in range(self.length):
            if self.orientation == Orientation.HORIZONTAL:
                location.append((row, col + i))
            else:
                location.append((row + i, col))

        self.location = location


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

        board.add_vehicle(Vehicle(car_name, orientation, start_col, start_row, length))

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

    print(board.locations)


if __name__ == '__main__':
    main()
