import csv

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .vehicle import Orientation


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
    def __init__(self, size: int) -> None:
        """
        Initializes the Board with a size, applicable to both its width and length. 
        Also sets up a dictionary to store vehicles (vehicle names as keys and 
        vehicle objects as values), a list to track the movement steps of vehicles 
        (vehicle names and step sizes as tuples), and an empty 2-D array to 
        represent the Board's layout.
        """
        self.size = size
        self.vehicles = {}
        self.steps = []
        self.locations = np.zeros((self.size, self.size), dtype='object')

    def add_vehicle(self, vehicle: object) -> None:
        """
        Adds a Vehicle to the Board by storing it in the vehicles dictionary and 
        updating the Board's layout to include the Vehicle's position.
        """
        name: str = vehicle.name
        self.vehicles[name] = vehicle

        # save the rows and columns occupied by the vehicle
        coords: list[tuple] = vehicle.location
        self.update_locations(coords, name)

    def update_locations(self, coords: list[tuple], name: str) -> None:
        """
        Updates the Board's layout by placing the name of the Vehicle on the 
        position.
        """
        for i in range(len(coords)):
            row, col = coords[i]

            self.locations[row, col] = name

    def check_move_forwards(self, vehicle: object) -> int:
        """
        Counts the number of possible steps a Vehicle can make forward until 
        collision with another Vehicle happens or the boundary is detected, 
        and returns the number of possible steps.
        """
        board_boundary: int = self.size - 1
        unoccupied: int = 0
        orientation: object = vehicle.orientation
        row_vehicle_front, col_vehicle_front = vehicle.location[-1]

        if orientation == Orientation.HORIZONTAL:
            possible_steps: int = board_boundary - col_vehicle_front

            # calculate the possible steps until a barrier occurs
            for step in range(1, possible_steps + 1):
                if self.locations[row_vehicle_front, col_vehicle_front + step] != unoccupied:
                    return step - 1

        else:
            possible_steps: int = board_boundary - row_vehicle_front

            # calculate the possible steps until a barrier occurs
            for step in range(1, possible_steps + 1):
                if self.locations[row_vehicle_front + step, col_vehicle_front] != unoccupied:
                    return step - 1

        return possible_steps

    def check_move_backwards(self, vehicle: object) -> int:
        """
        Counts the number of possible steps a Vehicle can make backward until 
        collision with another Vehicle happens or the boundary is detected, 
        and returns the number of possible steps.
        """
        unoccupied: int = 0
        orientation: object = vehicle.orientation
        row_vehicle_back, col_vehicle_back = vehicle.location[0]

        if orientation == Orientation.HORIZONTAL:
            possible_steps: int = col_vehicle_back

            # calculate the possible steps until a barrier occurs
            for step in range(1, possible_steps + 1):
                if self.locations[row_vehicle_back, col_vehicle_back - step] != unoccupied:
                    return step - 1
        else:
            possible_steps: int = row_vehicle_back

            # calculate the possible steps until a barrier occurs
            for step in range(1, possible_steps + 1):
                if self.locations[row_vehicle_back - step, col_vehicle_back] != unoccupied:
                    return step - 1

        return possible_steps

    def move_vehicle(self, vehicle: object, steps: int) -> None:
        """
        Checks if the Vehicle can be moved to the new location. If so, the 
        move of the Vehicle with its steps is saved and the Board's layout 
        is updated with the new location. Steps can be negative.
        """
        
        # check if a move is specified
        if steps == 0:
            raise ValueError

        # check if the desirable forward steps does not encounter a barrier
        if steps > 0:
            if steps > self.check_move_forwards(vehicle):
                raise ValueError
        
        # check if the desirable backward steps does not encounter a barrier
        else:
            if -steps > self.check_move_backwards(vehicle):
                raise ValueError

        old_coords: list[tuple] = vehicle.location
        row_vehicle_back, col_vehicle_back = old_coords[0]

        # save the new location of the vehicle for forward steps   
        if steps > 0:
            if vehicle.orientation == Orientation.HORIZONTAL:
                vehicle.update_location(col_vehicle_back + steps, row_vehicle_back)
            else:
                vehicle.update_location(col_vehicle_back, row_vehicle_back + steps)
        
        # save the new location of the vehicle for backward steps
        else:
            if vehicle.orientation == Orientation.HORIZONTAL:
                vehicle.update_location(col_vehicle_back + steps, row_vehicle_back)
            else:
                vehicle.update_location(col_vehicle_back, row_vehicle_back + steps)

        # save the move of the vehicle
        self.steps.append((vehicle.name, steps))

        # save the new rows and columns occupied by the vehicle
        self.update_locations(old_coords, 0)
        self.update_locations(vehicle.location, vehicle.name)

    def plot_board(self):
        available_colors = [
            'green',
            'yellow',
            'blue',
            'orange',
            'purple',
            'limegreen',
            'skyblue',
            'brown',
            'hotpink',
            'tomato',
            'magenta',
            'slateblue',
        ]

        fig, ax = plt.subplots()

        # draw gridlines
        ticks = np.arange(0, self.size + 1)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)

        ax.grid(linestyle='--', color='k', linewidth=1, zorder=0)

        ax.invert_yaxis()
        ax.set_aspect('equal')

        # draw patches
        for idx, vehicle in enumerate(self.vehicles.values()):
            num = idx % len(available_colors)
            color = available_colors[num]

            if vehicle.is_carter:
                color = 'red'

            rectangle = Rectangle(
                (vehicle.location[0][1], vehicle.location[0][0]),
                vehicle.length if vehicle.orientation == Orientation.HORIZONTAL else 1,
                vehicle.length if vehicle.orientation == Orientation.VERTICAL else 1,
                edgecolor='k',
                facecolor=color,
                fill=True,
                linewidth=2,
                zorder=5
            )

            ax.add_patch(rectangle)
            ax.annotate(
                vehicle.name,
                (0.5, 0.5),
                xycoords=rectangle,
                color='k',
                horizontalalignment='center',
                verticalalignment='center_baseline',
                zorder=10
            )

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
