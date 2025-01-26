from unittest.mock import patch, MagicMock

import pytest

from code.classes import (
    Board,
    CARTER_NAME,
    Orientation,
    Plotter,
    PlotterUnsupportedWriterError,
    Vehicle,
)


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
    assert plotter.fig is None
    assert plotter.ax is None
    assert isinstance(plotter.rectangles, dict)
    assert isinstance(plotter.annotations, dict)
    assert plotter.move_counter_text is None
    assert plotter.move_idx == 0


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

    assert plotter.fig is mock_fig
    assert plotter.ax is mock_ax

    mock_ax.set_xticks.assert_called_once()
    mock_ax.set_yticks.assert_called_once()

    xticks_args = mock_ax.set_xticks.call_args[0]
    yticks_args = mock_ax.set_yticks.call_args[0]

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
    dpi = 100

    plotter.plot_board(board, file_path, dpi)

    mock_fig.savefig.assert_called_once_with(file_path, dpi=dpi)
    mock_plt.show.assert_called_once()


@patch('code.classes.plotter.FuncAnimation')
@patch('code.classes.plotter.plt')
def test_animate_moves(
    mock_plt,
    mock_func_animation,
    plotter,
    board,
):
    """
    Test that animating moves works and calls the correct Matplotlib methods.
    """
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    moves = [
        ('A', 1),
        ('B', -1),
        (CARTER_NAME, 2),
    ]
    interval = 50

    plotter.animate_moves(
        MagicMock(board=board),
        moves,
        interval,
    )

    mock_func_animation.assert_called_once()

    animation_args, animation_kwargs = mock_func_animation.call_args

    assert animation_args[0] == plotter.fig
    assert callable(animation_args[1])
    assert animation_kwargs['frames'] == len(moves)
    assert animation_kwargs['interval'] == interval
    assert animation_kwargs['repeat'] is False

    mock_plt.show.assert_called_once()


@pytest.mark.parametrize('writer', ['pillow', 'ffmpeg'])
@patch('code.classes.plotter.FFMpegWriter')
@patch('code.classes.plotter.PillowWriter')
@patch('code.classes.plotter.FuncAnimation')
@patch('code.classes.plotter.plt')
def test_animate_moves_file_path(
    mock_plt,
    mock_func_animation,
    mock_pillow_writer,
    mock_ffmpeg_writer,
    plotter,
    board,
    writer,
):
    """
    Test that animating moves works and calls the correct Matplotlib methods.
    """
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)
    mock_pillow_writer_instance = mock_pillow_writer.return_value
    mock_ffmpeg_writer_instance = mock_ffmpeg_writer.return_value

    moves = [
        ('A', 1),
        ('B', -1),
        (CARTER_NAME, 2),
    ]
    interval = 50
    file_path = 'test_animation.gif'

    plotter.animate_moves(
        MagicMock(board=board),
        moves,
        interval,
        file_path,
        writer,
    )

    mock_func_animation.assert_called_once()

    animation_args, animation_kwargs = mock_func_animation.call_args

    assert animation_args[0] == plotter.fig
    assert callable(animation_args[1])
    assert animation_kwargs['frames'] == len(moves)
    assert animation_kwargs['interval'] == interval
    assert animation_kwargs['repeat'] is False

    assert mock_func_animation.return_value.save.called

    if writer == 'pillow':
        mock_func_animation.return_value.save.assert_called_once_with(
            file_path,
            mock_pillow_writer_instance
        )

    if writer == 'ffmpeg':
        mock_func_animation.return_value.save.assert_called_once_with(
            file_path,
            mock_ffmpeg_writer_instance
        )


@patch('code.classes.plotter.FuncAnimation')
@patch('code.classes.plotter.plt')
def test_animate_moves_file_path_wrong_writer(
    mock_plt,
    mock_func_animation,
    plotter,
    board
):
    """
    Test that animating moves raises an exception for unsupported writer types.
    """
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    moves = [
        ('A', 1),
        ('B', -1),
        (CARTER_NAME, 2),
    ]
    interval = 50

    with pytest.raises(PlotterUnsupportedWriterError) as exc:
        plotter.animate_moves(
            MagicMock(board=board),
            moves,
            interval,
            'test_animation.gif',
            'fail_writer',
        )

    assert 'unsupported writer type' in str(exc.value)
