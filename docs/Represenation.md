# Representation and assumptions

## The game

The game revolves around placing a number of vehicles on a square grid game board. Vehicles can be either 2 grid units long, representing cars, or 3 grid units long, representing trucks. Every game features one red car, 2 units long, which we’ve named **Carter**. The rules are simple: every vehicle is placed on the board with its front either facing right (horizontal orientation) or facing down (vertical orientation). Once placed in their starting positions, vehicles can only move forward or backward within their respective row or column. Vehicles cannot be placed on top of each other, nor can they cross one another.

The objective of the game is to move Carter forward until it reaches the border of the game board. Players can move only one vehicle at a time, and each move can be in either a forward or backward direction. The number of steps a vehicle can move is limited only by the number of available spots immediately in front of or behind it. Every move counts as a step, and the goal is to get Carter out of the board in the least number of steps.


## Representation choices

We're implementing this game and its solvers using Python, following the object-oriented programming (OOP) paradigm.

Our current setup includes two primary classes: the `Board` class and the `Vehicle` class. The `Board` class represents the game board, which is initialized with a specific size and is currently responsible for managing the placement and movement of vehicles.
The `Vehicle` class defines individual vehicle objects, tracking attributes such as their name, length, orientation, and current position on the board. This separation will hopefully allow us to handle the game mechanics in a modular way, making it easier to implement solvers and quickly test different configurations.


### Board

- The game board is represented as a 2D grid where each cell corresponds to a position on the board.
- Vehicles are identified by unique names, and their positions are determined by their starting position (coordinates for the back of the vehicle), length, and orientation (horizontal or vertical).

#### Game State

- In our current implementation, the board keeps track of the game state, which includes:
    - A list of vehicles.
    - The current board configuration.
    - The history of moves for tracking steps, number of moves, and exporting.

### Vehicle

- Each vehicle is represented as an object with attributes for:
    - Unique name.
    - Orientation (`HORIZONTAL` or `VERTICAL`).
    - Length (2 or 3 grid units).
    - Starting position (column and row).

### Moves

- Moves are represented as tuples containing:
    - The vehicle to be moved.
    - The number of steps to move (positive for forward, negative for backward).


## Assumptions

### Carter

- The red car, Carter, can only be placed in a horizontal orientation

### Moves

- A forward move is indicated by a positive integer, and a backward move by a negative integer.
- Forward moves are calculated from the coordinates of the front of the vehicle, while backward moves are calculated from the coordinates of the back of the vehicle.

### Valid moves only

- Vehicles can only move along their orientation (horizontal or vertical) and cannot jump rows or columns respectively.
- Moves are blocked by other vehicles or the edges of the board.
- Vehicles can't be placed on top of each other.
- Vehicles can't jump over or pass through a vehicle blocking their path.

### Game end

- The game ends when Carter reaches or is placed on the outermost grid square in front of it.
- This last move counts towards the number of moves.
