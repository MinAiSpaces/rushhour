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


def check_or_create_dir(path_name: str) -> None:
    """
    Helper function for checking if a folder exists and if it doesn't to create it
    """
    if not os.path.exists(path_name):
        os.makedirs(path_name)

