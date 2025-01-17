import os


def get_path(*args: str) -> str:
    """
    Helper function for getting the full path of a file or folder in this project
    """
    current_dir = os.path.dirname(__file__)

    return str(os.path.join(current_dir, *args))


def get_data_path() -> str:
    """
    Helper function for getting the full path of the 'data' folder in this project
    """
    return get_path('..', 'data')


def get_input_path() -> str:
    """
    Helper function for getting the full path of the 'input' folder in this project
    """
    return get_path('..', 'data', 'input')


def get_output_path() -> str:
    """
    Helper function for getting the full path of the 'output' folder in this project
    """
    return get_path('..', 'data', 'output')


def get_board_size_from_filename(filename: str) -> int:
    """
    Get the size of the board from the filename.
    Filename example: 'Rushhour6x6_1.csv'.
    """
    name_first_part = filename.split('_')[0]

    return int(name_first_part.lower().split('x')[1])
