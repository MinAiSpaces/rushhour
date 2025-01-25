import pytest

from code.classes import Vehicle, Orientation


@pytest.fixture(params=[
    {
        'name': 'A',
        'orientation': Orientation.HORIZONTAL,
        'start_col': 2,
        'start_row': 3,
        'length': 2,
    },
    {
        'name': 'B',
        'orientation': Orientation.VERTICAL,
        'start_col': 4,
        'start_row': 2,
        'length': 2,
    },
    {
        'name': 'X',
        'orientation': Orientation.HORIZONTAL,
        'start_col': 1,
        'start_row': 0,
        'length': 3,
    },
])
def vehicle(request):
    """
    Create test vehicles using the above declared values.
    """
    return Vehicle(**request.param)


def test_vehicle_initialization(vehicle):
    """
    Test vehicle initialization.
    """
    assert isinstance(vehicle, Vehicle)

    assert vehicle.length > 0
    assert vehicle.location is not None


def test_vehicle_location(vehicle):
    """
    Test if vehicle location is correctly calculated.
    """
    if vehicle.orientation == Orientation.HORIZONTAL:
        assert vehicle.location == [
            (vehicle.start_col + i, vehicle.start_row)
            for i in range(vehicle.length)
        ]
    else:
        assert vehicle.location == [
            (vehicle.start_col, vehicle.start_row + i)
            for i in range(vehicle.length)
        ]

    assert len(vehicle.location) == vehicle.length


def test_vehicle_is_carter(vehicle):
    """
    Test if Carter is correctly identified.
    """
    if vehicle.name == 'X':
        assert vehicle.is_carter is True
    else:
        assert vehicle.is_carter is False


def test_vehicle_update_location(vehicle):
    """
    Test updating the location of vehicles.
    """
    new_col = 3
    new_row = 2

    vehicle.update_location(new_col, new_row)

    if vehicle.orientation == Orientation.HORIZONTAL:
        assert vehicle.location == [
            (new_col + i, new_row)
            for i in range(vehicle.length)
        ]
    elif vehicle.orientation == Orientation.VERTICAL:
        assert vehicle.location == [
            (new_col, new_row + i)
            for i in range(vehicle.length)
        ]
