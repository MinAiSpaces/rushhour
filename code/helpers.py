import os


def get_path(*args):
    current_dir = os.path.dirname(__file__)

    return os.path.join(current_dir, *args)


def get_data_path():
    return get_path('..', 'data')


def get_input_path():
    return get_path('..', 'data', 'input')


def get_output_path():
    return get_path('..', 'data', 'output')


def check_or_create_dir(path_name):
    if not os.path.exists(path_name):
        os.makedirs(path_name)

