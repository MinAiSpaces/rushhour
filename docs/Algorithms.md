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

---

## A-Star

### Algorithm 1: A-Star with num blocking vehicles and max steps

#### Description

- ##### Selection Process

    - Take the board state with lowest score from heapqueue.
    - Check if the path for Carter is free to finish the game and make this move if so.
    - All maximum moves are collected and stored in a list of tuples.
    - For every maximum moves found, save the new state and score if not seen before.

- ##### Score calculation

    ```pseudocode
    Score = depth + 1 + number vehicles blocking carter in the front
    ```

- ##### Implementation

```pseudocode
while queue is not empty or game is not finished:
    pop best board state from heapqueue
    move carter if this finishes the game
    else:
        for every max move:
            create child
            create score and save in heapqueue if child is not seen before
```

### Algorithm 2: A-Star with num blocking vehicles and all available valid moves

#### Description

- ##### Selection Process

    - Take the board state with lowest score from heapqueue.
    - Check if the path for Carter is free to finish the game and make this move if so.
    - All available valid moves are collected and stored in a list of tuples.
    - For every available valid move found, save the new state and score if not seen before.

- ##### Score calculation

    ```pseudocode
    Score = depth + 1 + number vehicles blocking carter in the front
    ```

- ##### Implementation

```pseudocode
while queue is not empty or game is not finished:
    pop best board state from heapqueue
    move carter if this finishes the game
    else:
        for every available valid move:
            create child
            create score and save in heapqueue if child is not seen before
```

### Algorithm 3: A-Star with num two blocking vehicles and max steps

#### Description

- ##### Selection Process

    - Take the board state with lowest score from heapqueue.
    - Check if the path for Carter is free to finish the game and make this move if so.
    - All maximum moves are collected and stored in a list of tuples.
    - For every maximum moves found, save the new state and score if not seen before.

- ##### Score calculation

    ```pseudocode
    Score = depth + 1 + number vehicles blocking carter in the front + number vehicles blocking those vehicles
    ```

- ##### Implementation

```pseudocode
while queue is not empty or game is not finished:
    pop best board state from heapqueue
    move carter if this finishes the game
    else:
        for every max move:
            create child
            create score and save in heapqueue if child is not seen before
```

### Algorithm 4: A-Star with num two blocking vehicles and all available valid moves

#### Description

- ##### Selection Process

    - Take the board state with lowest score from heapqueue.
    - Check if the path for Carter is free to finish the game and make this move if so.
    - All available valid moves are collected and stored in a list of tuples.
    - For every available valid move found, save the new state and score if not seen before.

- ##### Score calculation

    ```pseudocode
    Score = depth + 1 + number vehicles blocking carter in the front + number vehicles blocking those vehicles
    ```

- ##### Implementation

```pseudocode
while queue is not empty or game is not finished:
    pop best board state from heapqueue
    move carter if this finishes the game
    else:
        for every available valid move:
            create child
            create score and save in heapqueue if child is not seen before
```