import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

from .vehicle import Orientation
from .board import Board


class PlotterError(ValueError):
    def __init__(self, message: str = 'PlotterError'):
        super().__init__(message)


class PlotterUnsupportedWriterError(PlotterError):
    def __init__(self, writer: str):
        super().__init__(f"'{writer}': unsupported writer type")


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
        self.fig = None
        self.ax = None
        self.rectangles = {}
        self.annotations = {}
        self.move_counter_text = None
        self.move_idx: int = 0

    def _initialize_plot(self, board: Board):
        """
        Initialize the board plot:
        - Draws dashed grid lines
        - Ensures grid is square
        - Inverts the y-axis
        - Picks a color from 'self.colors' to color the vehicles
        - Draws rectangles representing the vehicles
        - Annotates the vehicle with the vehicles name in its center
        """
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.clear()

        # Configure the grid
        self.ax.grid(linestyle='--', color='k', linewidth=1, zorder=0)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()

        # Set labels of the axes and the corresponding gridlines
        ticks = np.arange(0, board.size + 1)

        self.ax.set_xticks(ticks)
        self.ax.set_yticks(ticks)

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
            self.ax.add_patch(rectangle)
            self.rectangles[vehicle.name] = rectangle

            annotation = self.ax.annotate(
                vehicle.name,
                (0.5, 0.5),
                xycoords=rectangle,
                color='k',
                weight='bold',
                fontsize=12,
                horizontalalignment='center',
                verticalalignment='center_baseline',
                zorder=10
            )
            self.annotations[vehicle.name] = annotation

    def plot_board(
        self,
        board: Board,
        file_path: str | None = None,
        dpi: int = 300,
    ):
        """
        Plot the current state of the game board
        if file_path is not None, save the plot to file_path
        """
        self._initialize_plot(board)

        if file_path:
            self.fig.savefig(file_path, dpi=dpi)

        plt.show()

    def animate_moves(
        self,
        game: 'Game',
        moves: list[tuple[str, int]],
        interval: int = 500,
        file_path: str | None = None,
        writer_type: str = 'pillow',
        verbose: bool = False,
    ):
        """
        Animate moves on the board.

        Only moves the rectangle corresponding with the vehicle to be moved
        so we dont need to redraw every vehicle on every 'frame'

        The writer_type is used for saving the animation ('pillow', 'ffmpeg').
            - Use Pillow to generate gifs
            - Use ffmpeg to generate mp4 (videos)

        NB.
        Replays all moves using the Game class so board needs to be in
        correct 'start state' or we'll run into move conflicts.

        Added a move_idx because animation framerate was causing moves to
        be skipped and this obviously caused move conflicts as it tried to
        apply moves to vehicles that couldn't be moved in that order.
        """
        self._initialize_plot(game.board)

        # We need this to make sure the moves are made in order
        self.move_idx = 0

        # Placeholder for move counter text
        self.move_counter_text = self.ax.text(
            1.00,
            1.05,
            '',
            transform=self.ax.transAxes,
            color='k',
            weight='bold',
            fontsize=12,
            horizontalalignment='right',
            verticalalignment='center_baseline',
            zorder=15
        )

        def update(_):  # pragma: no cover
            if self.move_idx >= len(moves):

                # No more moves to animate
                return

            vehicle_name, steps = moves[self.move_idx]

            if verbose:
                print(
                    f"Animating move {self.move_idx}: "
                    f"('{vehicle_name}', {steps})"
                )

            game.make_move((vehicle_name, steps))

            vehicle = game.board.vehicles[vehicle_name]

            new_position = vehicle.location[0]

            self.rectangles[vehicle_name].set_xy(new_position)

            self.move_counter_text.set_text(f'Move: {self.move_idx + 1}')

            self.move_idx += 1

        animation = FuncAnimation(
            self.fig,
            update,
            frames=len(moves),
            interval=interval,
            repeat=False,
        )

        if file_path:
            if writer_type == 'pillow':
                writer = PillowWriter(fps=1000 // interval)
            elif writer_type == 'ffmpeg':
                writer = FFMpegWriter(fps=1000 // interval)
            else:
                raise PlotterUnsupportedWriterError(writer_type)

            animation.save(file_path, writer)
        else:
            plt.show()
