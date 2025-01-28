import os


def get_path(*args: str) -> str:
    """
    Helper function for getting the full path of a file or folder in this
    project.
    """
    current_dir = os.path.dirname(__file__)

    return str(os.path.join(current_dir, *args))


def get_data_path() -> str:
    """
    Helper function for getting the full path of the 'data' folder in this
    project.
    """
    return get_path('..', 'data')


def get_input_path() -> str:
    """
    Helper function for getting the full path of the 'input' folder in this
    project.
    """
    return get_path(get_data_path(), 'input')


def get_experiment_path() -> str:
    """
    Helper function for getting the full path of the 'experiment' folder in this project
    """
    return get_path(get_data_path(), 'experiment')


def get_gameboards_path() -> str:
    """
    Helper function for getting the full path of the 'input/gameboards' folder
    in this project.
    """
    return get_path(get_input_path(), 'gameboards')


def get_test_boards_path() -> str:
    """
    Helper function for getting the full path of the 'input/test_boards' folder
    in this project.
    """
    return get_path(get_input_path(), 'test_boards')


def get_output_path() -> str:
    """
    Helper function for getting the full path of the 'output' folder in this
    project.
    """
    return get_path(get_data_path(), 'output')


def get_output_images_path() -> str:
    """
    Helper function for getting the full path of the 'output/images' folder in
    this project.
    """
    return get_path(get_output_path(), 'images')


def get_board_size_from_file_path(file_path: str) -> int:
    """
    Get the size of the board from the filename.

    Filename example: 'Rushhour6x6_1.csv'.
    """
    filename = os.path.split(file_path)[1]
    name_first_part = filename.split('_')[0]

    return int(name_first_part.lower().split('x')[1])
