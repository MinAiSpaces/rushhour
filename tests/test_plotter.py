from unittest.mock import patch, MagicMock

import pytest

from code.classes import Board, CARTER_NAME, Orientation, Vehicle
from code.classes.plotter import Plotter


@pytest.fixture(params=[6, 9, 12])
def board(request):
    """
    Fixture for boards with a few vehicles.
    """
    board = Board(request.param)

    vehicles = [
        Vehicle(
            'A',
            Orientation.HORIZONTAL,
            0,
            0,
            2,
        ),
        Vehicle(
            'B',
            Orientation.VERTICAL,
            2,
            1,
            3,
        ),
        Vehicle(
            CARTER_NAME,
            Orientation.HORIZONTAL,
            3,
            5,
            2,
        ),
    ]

    for vehicle in vehicles:
        board.add_vehicle(vehicle)

    return board


@pytest.fixture
def plotter():
    """
    Fixture for plotters.
    """
    return Plotter()


def test_plotter(plotter):
    """
    Test plotter initialization.
    """
    assert isinstance(plotter, Plotter)

    assert plotter.colors is not None


@patch('code.classes.plotter.Rectangle')
@patch('code.classes.plotter.plt')
def test_plot_board(mock_plt, mock_rectangle, plotter, board):
    """
    Test that plotting works and calls the correct Matplotlib methods.
    """
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    plotter.plot_board(board)

    mock_ax.set_xticks.assert_called_once()
    mock_ax.set_yticks.assert_called_once()

    xticks_args = mock_ax.set_xticks.call_args[0]
    yticks_args = mock_ax.set_xticks.call_args[0]

    assert len(xticks_args[0]) == board.size + 1
    assert len(yticks_args[0]) == board.size + 1

    assert mock_rectangle.call_count == len(board.vehicles)
    assert mock_ax.add_patch.call_count == len(board.vehicles)
    assert mock_ax.annotate.call_count == len(board.vehicles)

    mock_plt.show.assert_called_once()


@patch('code.classes.plotter.plt')
def test_plot_board_file_path(mock_plt, plotter, board):
    """
    Test that plotting works with file_path.
    """
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    file_path = 'test_output.png'

    plotter.plot_board(board, file_path)

    mock_fig.savefig.assert_called_once()

    savefig_args = mock_fig.savefig.call_args[0][0]

    assert savefig_args == file_path

    mock_plt.show.assert_called_once()
