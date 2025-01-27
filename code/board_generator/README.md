# Board generator

## Description

This is a very rudimentary exploration of a board generator. Turns out generating interesting boards is much harder than expected. This project was abandoned in favour of time.

## Usage
1. From the <rush_hour_folder_name>:
   ```bash
   cd <rush_hour_folder_name>
   ```
2. Run the generator
   ```bash
   python -m code.board_generator.board_generator
   ```

## Limitations
- Generated boards are not stored
- A very naive randomize algorithms is used to try to solve the generator board
- If a solution is found:
    - prints the number of moves it took the random algorithm to solve the board
    - prints the number of vehicles it was able to place on the board within the allowed number of iterations
- If no solution is found this will run indefinitely until the program is interrupted

    ```bash
    ctrl + c
    ```
