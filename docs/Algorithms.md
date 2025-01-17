# Algorithms

## Randomization

### Algorithm 1: Uniform randomization of all available valid moves

### Description

- #### Selection Process

    - Before making a move, all available moves are collected and stored in a list of tuples.
    - A move is then selected at random from this list of all available valid moves.

- #### Implementation

```pseudocode
while no solution found:
    pick a random move from all available moves for current state
    perform the selected move
```

## Algorithm 2: Randomization vehicle first

### Description

- #### Selection Process

    - Before making a move, all available moves are collected and stored in a list of tuples.
    - From the list of available valid moves, the unique vehicles are extracted.
    - A vehicle is then selected at random from this list of vehicles.
    - Finally, a valid move for this vehicle is selected at random from the list of available valid moves for this vehicle.

- ### Implementation

```pseudocode
while no solution found:
    find all available moves for current state
    collect all unique vehicles from the available moves
    randomly select a vehicle from these unique vehicles
    pick a random move for selected vehicle
    perform the selected move
```
