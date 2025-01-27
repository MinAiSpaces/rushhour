import csv

from code.classes import Orientation, Game


def read_board_state_from_csv(
    file_path: str
) -> list[tuple[str, Orientation, int, int, int]]:
    """
    Read game board setup from CSV file.

    Creates a list of vehicle data for each row.
    This data can then be used as input for setting up a game for example.
    """
    data: list[tuple[str, Orientation, int, int, int]] = []

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)

        # Converts values to correct data types for use and consistency
        for data_row in reader:
            car_name = data_row['car'].upper()
            orientation = data_row['orientation'].upper()
            col = int(data_row['col'])
            row = int(data_row['row'])
            length = int(data_row['length'])

            # Change col and row to be 0 indexed instead of 1 indexed
            start_col = col - 1
            start_row = row - 1
            orientation = (
                Orientation.HORIZONTAL
                if orientation == 'H'
                else Orientation.VERTICAL
            )

            data.append((car_name, orientation, start_col, start_row, length))

    return data


def write_moves_to_csv(file_path: str, moves: list[tuple[str, int]]) -> None:
    """
    Write moves to a CSV file.

    Writes a header row consisting of the fieldnames
    And a row for every move containing:
        - the vehicle name
        - the steps (positive for forwards, negative for backwards)
    """
    with open(file_path, 'w', newline='') as f:
        fieldnames = ['car', 'move']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for vehicle_name, steps in moves:
            writer.writerow({
                'car': vehicle_name,
                'move': steps
            })


def read_moves_from_csv(file_path) -> list[tuple[str, int]]:
    """
    Read moves from a CSV file.

    Creates a list of moves data for each row.
    """
    data: list[tuple[str, int]] = []

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)

        for move in reader:
            data.append((move['car'].upper(), int(move['move'])))

    return data


def generate_results(results: list[tuple[int, float, int | str, int | str]], dest_file: str) -> None:
    """
    Writes all the search results (number of moves made, solving time, number of
    seen states, max size of queue) to a CSV file.
    """
    with open(dest_file, 'w', newline='') as f:
        fieldnames = ['number moves made', 'solving time', 'number seen states', 'max_queue_size']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for num_moves_made, solving_time, num_seen_states, max_queue_size in results:
            writer.writerow({
                    'number moves made': num_moves_made,
                    'solving time': solving_time,
                    'number seen states': num_seen_states,
                    'max_queue_size': max_queue_size
            })
