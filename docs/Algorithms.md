# Algorithms

## Randomization

### Algorithm 1: Uniform randomization of all available valid moves

#### Description

- ##### Selection Process

    - Before making a move, all available moves are collected and stored in a list of tuples.
    - A move is then selected at random from this list of all available valid moves.

- ##### Implementation

```pseudocode
while no solution found:
    pick a random move from all available moves for current state
    perform the selected move
```

### Algorithm 2: Randomization vehicle first

#### Description

- ##### Selection Process

    - Before making a move, all available moves are collected and stored in a list of tuples.
    - From the list of available valid moves, the unique vehicles are extracted.
    - A vehicle is then selected at random from this list of vehicles.
    - Finally, a valid move for this vehicle is selected at random from the list of available valid moves for this vehicle.

- ##### Implementation

```pseudocode
while no solution found:
    find all available moves for current state
    collect all unique vehicles from the available moves
    randomly select a vehicle from these unique vehicles
    pick a random move for selected vehicle
    perform the selected move
```

### Algorithm 3: Uniform randomization of all available valid moves with finish check

#### Description

- ##### Selection Process

    - Check if the path for Carter is free to finish the game and make this move if so.
    - Before making a move, all available moves are collected and stored in a list of tuples.
    - A move is then selected at random from this list of all available valid moves.

- ##### Implementation

```pseudocode
while no solution found:
    check if carter is free
    if carter is free:
        make carter move to finish the game
    else:
        pick a random move from all available moves for current state
        perform the selected move
```

### Algorithm 4: Uniform randomization without double vehicles of all max steps with finish check

#### Description

- ##### Selection Process

    - Check if the path for Carter is free to finish the game and make this move if so.
    - Before making a move, all maximum moves are collected and stored in a list of tuples.
    - A move is then selected at random from this list of all maximum valid moves.
    - If the vehicle is not the same as the last moved vehicle, execute the move.

- ##### Implementation

```pseudocode
while no solution found:
    check if carter is free
    if carter is free:
        make carter move to finish the game
    else:
        pick a random move from all maximum moves for current state

        if vehicle is not the same as last moved vehicle:
            perform the selected move and save moved vehicle
```
