import csv

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .vehicle import Vehicle, Orientation


class Board:
    """
    This class creates a new Board object when it is called and keeps track of all the 
    moves of the Vehicles in an internal representation, with the names of all the Vehicle 
    objects displayed at their corresponding locations. 
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
        self.vehicles: dict[str, Vehicle] = {}
        self.steps: list[tuple[str, int]] = []
        self.locations = np.zeros((self.size, self.size), dtype='object')

    def add_vehicle(self, vehicle: Vehicle) -> None:
        """
        Adds a Vehicle to the Board by storing it in the vehicles dictionary and 
        updating the Board's layout to include the Vehicle's position.
        """
        name: str = vehicle.name
        self.vehicles[name] = vehicle

        # save the rows and columns occupied by the vehicle
        coords: list[tuple[int, int]] = vehicle.location
        self.update_locations(coords, name)

    def update_locations(self, coords: list[tuple[int, int]], name: str) -> None:
        """
        Updates the Board's layout by storing the name of the Vehicle on the 
        coordinates.
        """
        for i in range(len(coords)):
            row, col = coords[i]

            self.locations[row, col] = name

    def check_move_forwards(self, vehicle: Vehicle) -> int:
        """
        Counts the number of possible steps a Vehicle can make forward until 
        collision with another Vehicle happens or the boundary is detected, 
        and returns the number of possible steps.
        """
        board_boundary: int = self.size - 1
        unoccupied: int = 0
        orientation: Orientation = vehicle.orientation
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

    def check_move_backwards(self, vehicle: Vehicle) -> int:
        """
        Counts the number of possible steps a Vehicle can make backward until 
        collision with another Vehicle happens or the boundary is detected, 
        and returns the number of possible steps.
        """
        unoccupied: int = 0
        orientation: Orientation = vehicle.orientation
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

    def move_vehicle(self, vehicle: Vehicle, steps: int) -> bool:
        """
        Checks if the Vehicle can be moved to the new location. If so, the 
        move of the Vehicle with its steps is saved and the Board's layout 
        is updated with the new location. Steps can be negative.
        Returns True if carter is in front of the exit.
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

        old_coords: list[tuple[int, int]] = vehicle.location
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

        if vehicle.is_carter:
            return self.check_game_finished()

        return False

    def plot_board(self) -> None:
        """
        Draws the Board with its size and the gridlines, and colors the 
        locations of the Vehicles on the Board's layout with distinctive 
        colors.
        """
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

        # set the labels of the axes and the corresponding gridlines
        ticks = np.arange(0, self.size + 1)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.grid(linestyle='--', color='k', linewidth=1, zorder=0)

        ax.invert_yaxis()

        # make the board square
        ax.set_aspect('equal')

        for idx, vehicle in enumerate(self.vehicles.values()):

            # prevent adjacent vehicles from having the same color
            num = idx % len(available_colors)
            color = available_colors[num]

            if vehicle.is_carter:
                color = 'red'

            # create the vehicle's patch over the grid
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

            # place the vehicle's name in the middle of the patch
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

    def export_steps(self, dest_file: str) -> None:
        """
        Exports all the moves of all the Vehicles to a destinated csv file.
        """
        with open(dest_file, 'w', newline='') as f:
            fieldnames = ['car', 'move']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # add the name of the vehicle and its step size as a row
            for step in self.steps:
                writer.writerow({
                    'car': step[0],
                    'move': step[1]
                })

    def check_game_finished(self) -> bool:
        """
        Returns True if carter stands in front of the exit.
        """
        carter: Vehicle = self.vehicles['X']
        board_boundary: int = self.size - 1

        if self.locations[carter.start_row, board_boundary] == 'X':
            return True

        return False
