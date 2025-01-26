import numpy as np
import pytest

from code.classes import (
    Board,
    BoardPlacementOutOfBoundsError,
    BoardPlacementOccupiedError,
    BoardVehicleNameExistError,
    BoardVehicleCarterOrientationError,
    CARTER_NAME,
    Orientation,
    Vehicle,
)


@pytest.fixture(params=[6, 9, 12])
def board(request):
    """
    Fixture for creating different sized boards.
    """
    return Board(request.param)


@pytest.fixture
def valid_vehicles():
    """
    Fixture for creating a list of valid test vehicles.
    """
    return [
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
            2,
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


def test_board_initialization(board):
    """
    Test board initialization.
    """
    assert isinstance(board, Board)

    assert board.size in [6, 9, 12]
    assert isinstance(board.vehicles, dict)


def test_board_locations(board):
    """
    Test if board locations __post_init__ works.
    """
    assert board.locations.shape == (board.size, board.size)
    assert board.locations.sum() == 0


def test_add_vehicle_success(board, valid_vehicles):
    """
    Test successfully adding vehicles to the board.
    """
    assert len(board.vehicles) == 0

    for vehicle in valid_vehicles:
        board.add_vehicle(vehicle)

        vehicle_name = vehicle.name
        start_col = vehicle.start_col
        start_row = vehicle.start_row
        length = vehicle.length

        if vehicle.orientation == Orientation.HORIZONTAL:
            assert np.all(
                board.locations[start_row, start_col:start_col + length]
            ) == vehicle_name
        else:
            assert np.all(
                board.locations[start_row:start_row + length, start_col]
            ) == vehicle_name

    assert len(board.vehicles) == len(valid_vehicles)


def test_add_vehicle_name_exists_error(board, valid_vehicles):
    """
    Test adding a vehicle with same name raises an error.
    """
    for vehicle in valid_vehicles:
        vehicle_name = vehicle.name

        board.add_vehicle(vehicle)

        with pytest.raises(BoardVehicleNameExistError) as exc:
            board.add_vehicle(vehicle)

        assert (
            f"Vehicle '{vehicle_name}': "
            f"a vehicle with this name already exists"
            in str(exc.value)
        )


def test_add_vehicle_carter_orientation_error(board):
    """
    Test adding Carter not in horizontal orientation raises an error.
    """
    fail_carter = Vehicle(
        CARTER_NAME,
        Orientation.VERTICAL,
        0,
        0,
        2,
    )

    with pytest.raises(BoardVehicleCarterOrientationError) as exc:
        board.add_vehicle(fail_carter)

    assert (
        f"Vehicle '{CARTER_NAME}': Carter can only be placed horizontally"
        in str(exc.value)
    )


@pytest.mark.parametrize('length', [2, 3])
def test_add_vehicle_out_of_bounds_error_horizontal(board, length):
    """
    Test placing vehicle out of bounds horizontally raises an error.
    """
    # Just within bounds
    success_horizontal = Vehicle(
        'A',
        Orientation.HORIZONTAL,
        board.size - length,
        3,
        length,
    )

    # Out of bounds
    fail_horizontal = Vehicle(
        'B',
        Orientation.HORIZONTAL,
        board.size - 1,
        0,
        length,
    )

    board.add_vehicle(success_horizontal)

    with pytest.raises(BoardPlacementOutOfBoundsError) as exc:
        board.add_vehicle(fail_horizontal)


@pytest.mark.parametrize('length', [2, 3])
def test_add_vehicle_out_of_bounds_error_vertical(board, length):
    """
    Test placing vehicle out of bounds vertically raises an error.
    """
    # Just within bounds
    success_vertical = Vehicle(
        'A',
        Orientation.VERTICAL,
        3,
        board.size - length,
        length,
    )

    # Out of bounds
    fail_vertical = Vehicle(
        'B',
        Orientation.VERTICAL,
        0,
        board.size - 1,
        length,
        )

    board.add_vehicle(success_vertical)

    with pytest.raises(BoardPlacementOutOfBoundsError) as exc:
        board.add_vehicle(fail_vertical)


def test_add_vehicle_occupied_error(board, valid_vehicles):
    """
    Test adding a vehicle on top of another vehicle raises an error.
    """
    start_col = valid_vehicles[0].start_col
    start_row = valid_vehicles[0].start_row
    length = valid_vehicles[0].length

    # Add first vehicle at (0, 0)
    board.add_vehicle(valid_vehicles[0])

    # Just behind first vehicle
    success_vehicle = Vehicle(
        'D',
        Orientation.HORIZONTAL,
        start_col + length,
        start_row,
        2,
    )

    # On top of second vehicle
    fail_vehicle = Vehicle(
        'E',
        Orientation.HORIZONTAL,
        success_vehicle.start_col + length - 1,
        start_row,
        2,
    )

    board.add_vehicle(success_vehicle)

    with pytest.raises(BoardPlacementOccupiedError) as exc:
        board.add_vehicle(fail_vehicle)

    assert (
        f"Vehicle '{fail_vehicle.name}': "
        f"placement is on top of another vehicle"
        in str(exc.value)
    )


@pytest.mark.parametrize('length', [2, 3])
def test_add_vehicle_occupied_error_mixed(board, valid_vehicles, length):
    """
    Test adding a vehicle on top of another vehicle raises an error.
    """
    start_col = valid_vehicles[1].start_col
    start_row = valid_vehicles[1].start_row
    length = valid_vehicles[1].length

    # Add first vehicle vertically at (2, 2)
    board.add_vehicle(valid_vehicles[1])

    # Add second vehicle at (3, 2)
    success_vehicle = Vehicle(
        'D',
        Orientation.HORIZONTAL,
        start_col + 1,
        start_row,
        length,
    )

    # On top of first vehicle (2, 3)
    fail_vehicle = Vehicle(
        'E',
        Orientation.HORIZONTAL,
        start_col - 1,
        start_row + 1,
        length,
    )

    board.add_vehicle(success_vehicle)

    with pytest.raises(BoardPlacementOccupiedError) as exc:
        board.add_vehicle(fail_vehicle)

    assert (
        f"Vehicle '{fail_vehicle.name}': "
        f"placement is on top of another vehicle"
        in str(exc.value)
    )


def test_update_state_not_new(board, valid_vehicles):
    """
    Test updating the state without 'new' flag.
    """
    start_col = valid_vehicles[0].start_col
    start_row = valid_vehicles[0].start_row
    length = valid_vehicles[0].length

    # Add first horizontally at (0, 0)
    board.add_vehicle(valid_vehicles[0])

    assert np.all(
        board.locations[start_row, start_col:start_col + length]
    ) == valid_vehicles[0].name

    # Manually move vehicle 2 steps horizontally
    steps = 2
    valid_vehicles[0].location = [
        (col + steps, row)
        for col, row in valid_vehicles[0].location
    ]

    board.update_state(valid_vehicles[0])

    assert np.all(
        board.locations[start_row, start_col:start_col + length]
    ) == 0

    new_col = start_col + steps
    assert np.all(
        board.locations[start_row, new_col:new_col + length]
    ) == valid_vehicles[0].name


def test_update_state_new(board, valid_vehicles):
    """
    Test updating the state with 'new' flag.
    """
    start_col = valid_vehicles[0].start_col
    start_row = valid_vehicles[0].start_row
    length = valid_vehicles[0].length

    # Add first horizontally at (0, 0)
    board.add_vehicle(valid_vehicles[0])

    assert np.all(
        board.locations[start_row, start_col:start_col + length]
    ) == valid_vehicles[0].name

    # Manually move vehicle 2 steps horizontally
    steps = 3
    valid_vehicles[0].location = [
        (col + steps, row)
        for col, row in valid_vehicles[0].location
    ]

    board.update_state(valid_vehicles[0], True)

    assert np.all(
        board.locations[start_row, start_col:start_col + length]
    ) == valid_vehicles[0].name

    new_col = start_col + steps
    assert np.all(
        board.locations[start_row, new_col:new_col + length]
    ) == valid_vehicles[0].name

