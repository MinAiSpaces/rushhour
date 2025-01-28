import copy

from code.algorithms import all_max_moves_finish_check
from code.classes import Game
from code.helpers import get_gameboard_file_paths


def main():
    board = 2
    gameboards_paths = get_gameboard_file_paths()
    gameboards_dict = {
        idx + 1: gameboard_path
        for idx, gameboard_path in enumerate(gameboards_paths)
    }

    print(f'Loading board {board}')

    game = Game.load_game_from_csv(gameboards_dict[board])

    print(f'Board {board} loaded')

    print('Trying to solve board by randomly making moves')

    all_max_moves_finish_check(game)

    print(f'Solution found in {len(game.moves)} random moves!')

    moves = copy.copy(game.moves)

    game.reset()
    game.animate_moves(moves, interval=50)


if __name__ == '__main__':
    print("Let's play a game of Rush Hour!")

    main()
