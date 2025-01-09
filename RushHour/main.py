import os
from enum import Enum

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


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
        


        #https://stackoverflow.com/questions/43971138/python-plotting-colored-grid-based-on-values
        # data = np.random.rand(10, 10) * 20
        # create discrete colormap
        cmap = mcolors.ListedColormap(['green', 'yellow', 'blue', 'orange', 'purple', 'pink', 'grey', 'brown', 'beige', 'cyan', 'magenta'])
        # cmap = mcolors.ListedColormap(list(mcolors.CSS4_COLORS.keys())[:46])
        # bounds = [0,10,20]
        # norm = colors.BoundaryNorm(bounds, cmap.N)
        available_colors = ['green', 'yellow', 'blue', 'orange', 'purple', 'pink', 'grey', 'brown', 'beige', 'cyan', 'magenta']
        grid_colors = []

        color='white'
        for row in self.locations:
            for cell in row:

                if cell == -1:
                    color = 'red'
                elif cell == 0:
                    color = 'white'
                else:
                    num = (len(available_colors) - 1) % cell
                    print(num)
                    color = available_colors[num]
            
                grid_colors.append(color)

        cmap = mcolors.ListedColormap(grid_colors)
        print(cmap)
        fig, ax = plt.subplots()
        ax.imshow(self.locations, cmap=cmap)

        # draw gridlines
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        ax.set_xticks(np.arange(0, self.size+1, 1));
        ax.set_yticks(np.arange(0, self.size+1, 1));

        plt.show()



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


def setup_board(df_gameboard, board_size):
    board = Board(board_size)

    for car_name, orientation, start_col, start_row, length in zip(
            df_gameboard['car'],
            df_gameboard['orientation'],
            df_gameboard['col'],
            df_gameboard['row'],
            df_gameboard['length'],
    ):
        start_col -= 1
        start_row -= 1
        orientation = Orientation.HORIZONTAL if orientation == 'H' else Orientation.VERTICAL
        is_carter = car_name == 'X'

        board.add_vehicle(car_name, Vehicle(orientation, start_col, start_row, length, is_carter))

    return board


def load_board_from_csv(filename_path):
    df = pd.read_csv(filename_path)

    df['car'] = df['car'].apply(lambda x: x.upper())
    df['orientation'] = df['orientation'].apply(lambda x: x.upper())

    return df


def main():
    filename = 'RushHour6x6_1.csv'
    current_dir = os.path.dirname(__file__)
    filename_path = os.path.join(current_dir, '..', 'gameboards', filename)

    df_gameboard = load_board_from_csv(filename_path)

    board_size = get_board_size_from_filename(filename)

    board = setup_board(df_gameboard, board_size)

    print(board.locations)
    board.plot_board()


if __name__ == '__main__':
    main()
