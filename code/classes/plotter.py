import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .vehicle import Orientation
from .board import Board


class Plotter:
    """
    Plotter is responsible for visualizing the current state of the
    game board. It renders the grid, vehicles, and their positions.
    """
    def __init__(self):
        self.colors = [
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

    def plot_board(self, board: Board, file_path: str | None = None):
        """
        Plot the current state of the game board
        if file_path is not None, save the plot to file_path

        - Draws dashed grid lines
        - Ensures grid is square
        - Inverts the y-axis
        - Picks a color from 'self.colors' to color the vehicles
        - Draws rectangles representing the vehicles
        - Annotates the vehicle with the vehicles name in its center
        """
        fig, ax = plt.subplots(figsize=(8, 8))

        ax.grid(linestyle='--', color='k', linewidth=1, zorder=0)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        # Set labels of the axes and the corresponding gridlines
        ticks = np.arange(0, board.size + 1)

        ax.set_xticks(ticks)
        ax.set_yticks(ticks)

        for idx, vehicle in enumerate(board.vehicles.values()):
            color = self.colors[idx % len(self.colors)]

            if vehicle.is_carter:
                color = 'red'

            rectangle = Rectangle(
                vehicle.location[0],
                (
                    vehicle.length
                    if vehicle.orientation == Orientation.HORIZONTAL
                    else 1
                ),
                (
                    vehicle.length
                    if vehicle.orientation == Orientation.VERTICAL
                    else 1
                ),
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

        if file_path:
            fig.savefig(file_path, dpi=300)

        plt.show()
