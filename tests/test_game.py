from unittest.mock import patch, MagicMock

import pytest

from code.classes import (
    CARTER_NAME,
    Game,
    Orientation,
    SetupBoardNoCarterError,
    SetupBoardNoVehicleDataError,
)


@pytest.fixture
def game_data():
    """
    Fixture with game data.
    """
    return [
        ('A', Orientation.HORIZONTAL, 0, 0, 2),
        ('B', Orientation.VERTICAL, 2, 2, 3),
        (CARTER_NAME, Orientation.HORIZONTAL, 0, 2, 2),
    ]


@pytest.fixture
def moves():
    return [('A', 1), ('B', -1), (CARTER_NAME, 2)]


@pytest.mark.parametrize('board_size', [6, 9, 12])
@patch('code.classes.game.Board')
@patch('code.classes.game.Mover')
@patch('code.classes.game.Plotter')
def test_game(mock_plotter, mock_mover, mock_board, game_data, board_size):
    """
    Test game initialization.
    """
    mock_board_instance = mock_board.return_value
    mock_mover_instance = mock_mover.return_value
    mock_plotter_instance = mock_plotter.return_value

    game = Game(game_data, board_size)

    mock_board.assert_called_once_with(board_size)
    mock_mover.assert_called_once_with(game.board)
    mock_plotter.assert_called_once()

    assert game.board == mock_board_instance
    assert game.mover == mock_mover_instance
    assert game.plotter == mock_plotter_instance


@patch('code.classes.game.Mover')
def test_get_all_available_moves(mock_mover, game_data):
    """
    Test calling get_all_available_moves without specifying a vehicle.
    """
    mock_mover_instance = mock_mover.return_value
    mock_mover_instance.get_all_available_moves.return_value = [
        (CARTER_NAME, 1), ('A', -1)
    ]

    game = Game(game_data, 6)

    moves = game.get_all_available_moves()

    mock_mover_instance.get_all_available_moves.assert_called_once_with(None)
    assert moves == [(CARTER_NAME, 1), ('A', -1)]


@patch('code.classes.game.Mover')
def test_get_all_available_moves_vehicle(mock_mover, game_data):
    """
    Test calling get_all_available_moves with a vehicle.
    """
    mock_mover_instance = mock_mover.return_value
    mock_mover_instance.get_all_available_moves.return_value = [
        (CARTER_NAME, 1)
    ]

    game = Game(game_data, 6)

    moves = game.get_all_available_moves(CARTER_NAME)

    mock_mover_instance.get_all_available_moves.assert_called_once_with(
        CARTER_NAME
    )
    assert moves == [(CARTER_NAME, 1)]


@patch('code.classes.game.Mover')
def test_make_move(mock_mover, game_data):
    """
    Test the make_move method.
    """
    mock_mover_instance = mock_mover.return_value

    moves = [
        ('A', -1),
        (CARTER_NAME, 1),
    ]

    game = Game(game_data, 6)

    game.make_move(moves[0])
    game.make_move(moves[1])
    game.make_move(moves[0])

    assert mock_mover_instance.move_vehicle.call_count == 3
    assert len(game.moves) == 3
    assert game.moves == [moves[0], moves[1], moves[0]]


@patch('code.classes.game.Plotter')
def test_plot_board(mock_plotter, game_data):
    """
    Test plot_board calls the plotter with board only.
    """
    mock_plotter_instance = mock_plotter.return_value

    game = Game(game_data, 6)

    game.plot_board()

    mock_plotter_instance.plot_board.assert_called_once_with(
        game.board,
        None,
        300
    )


@patch('code.classes.game.Plotter')
def test_plot_board_file_path(mock_plotter, game_data):
    """
    Test plot_board calls the plotter with board and file_path.
    """
    mock_plotter_instance = mock_plotter.return_value

    file_path = 'test_output.png'

    game = Game(game_data, 6)

    game.plot_board(file_path)

    plot_board_args = mock_plotter_instance.plot_board.call_args[0]

    assert plot_board_args[1] == file_path


@patch('code.classes.game.Plotter')
def test_plot_board_dpi(mock_plotter, game_data):
    """
    Test plot_board calls the plotter with board and dpi.
    """
    mock_plotter_instance = mock_plotter.return_value

    file_path = 'test_output.png'
    dpi = 100

    game = Game(game_data, 6)

    game.plot_board(file_path, dpi)

    plot_board_args = mock_plotter_instance.plot_board.call_args[0]

    assert plot_board_args[2] == dpi


@patch('code.classes.game.Plotter')
def test_animate_moves(mock_plotter, game_data, moves):
    """
    Test animate_moves method calls the plotter with game.moves.
    """
    mock_plotter_instance = mock_plotter.return_value

    game = Game(game_data, 6)

    game.moves = moves

    game.animate_moves()

    mock_plotter_instance.animate_moves.assert_called_once_with(
        game,
        game.moves,
        500,
        None,
        'pillow',
        True,
    )


@pytest.mark.parametrize('writer', ['pillow', 'ffmpeg'])
@patch('code.classes.game.Plotter')
def test_animate_moves_supplied_moves(mock_plotter, writer, game_data, moves):
    """
    Test animate_moves method calls the plotter with supplied moves.
    """
    mock_plotter_instance = mock_plotter.return_value

    game = Game(game_data, 6)
    interval = 100
    file_path = 'test_animation.gif'

    game.animate_moves(
        moves,
        interval,
        file_path,
        writer,
        True,
    )

    assert len(game.moves) == 0

    mock_plotter_instance.animate_moves.assert_called_once_with(
        game,
        moves,
        interval,
        file_path,
        writer,
        True,
    )


@pytest.mark.parametrize('board_size', [6, 9, 12])
@patch('code.classes.game.Board')
def test_is_finished(mock_board, game_data, board_size):
    """
    Test static method to determine if the game is finished.
    """
    carter_locations = [
        (board_size - col, 3)
        for col in range(2, 0, -1)
    ]

    mock_board_instance = mock_board.return_value
    mock_board_instance.size = board_size
    mock_board_instance.vehicles = {
        CARTER_NAME: MagicMock(location=carter_locations),
    }

    game = Game(game_data, board_size)

    finished = Game.is_finished(game.board)

    assert finished is True


@patch('code.classes.game.Board')
def test_setup_board(mock_board, game_data):
    """
    Test static method setup_board returns a board.
    """
    mock_board_instance = mock_board.return_value
    mock_board_instance.vehicles = {
        data[0]: 'mock_vehicle'
        for data in game_data
    }

    board = Game.setup_board(mock_board_instance, game_data)

    assert board == mock_board_instance
    assert mock_board_instance.add_vehicle.call_count == len(game_data)


@patch('code.classes.game.Board')
def test_setup_board_no_data(mock_board):
    """
    Test static method setup_board with empty data raises error.
    """
    mock_board_instance = mock_board.return_value

    with pytest.raises(SetupBoardNoVehicleDataError) as exc:
        Game.setup_board(mock_board_instance, [])

    assert ('No vehicle data provided' in str(exc.value))


@patch('code.classes.game.Board')
def test_setup_board_no_carter(mock_board, game_data):
    """
    Test static method setup_board with empty data raises error.
    """
    no_carter = [game_data[0], game_data[1]]

    mock_board_instance = mock_board.return_value
    mock_board_instance.vehicles = {
        data[0]: 'mock_vehicle'
        for data in no_carter
    }

    with pytest.raises(SetupBoardNoCarterError) as exc:
        Game.setup_board(
            mock_board_instance,
            no_carter,
        )

    assert 'Carter appears to be missing on the board' in str(exc.value)
