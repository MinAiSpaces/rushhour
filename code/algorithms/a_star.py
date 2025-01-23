from code.classes import Board, Vehicle


def num_blocking_vehicles(state: Board) -> int:
    """
    Counts the number of vehicles directly blocking Carter in the front.
    """
    carter_row_num = state.vehicles['X'].start_row
    carter_row: np.ndarray[object] = state.locations[carter_row_num]

    idx_after_carter = state.vehicles['X'].location[-1][0] + 1

    return len({carter_row[i] for i in range(idx_after_carter, len(carter_row)) if carter_row[i] != 0})
