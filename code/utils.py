import csv

from code.classes import Orientation


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
