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
            for every valid max move:
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
    - For every maximum move found, save the new state and score if not seen before.

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
            for every valid max move:
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

---

## Breadth First

### Algorithm 1: Breadth First with max steps and without useful move check

#### Description

- ##### Selection Process
    - Take the first board state from queue.
    - Check if the path for Carter is free to finish the game and make this move if so.
    - All maximum moves are collected and stored in a list of tuples.
    - For every maximum move found, save the new state if not seen before.

- ##### Implementation

    ```pseudocode
    while queue is not empty and no finish is found:
        pop first board state from queue
        check if finish is reached
        move carter if this finishes the game
        else:
            for every valid max move:
                create child and save in queue if child is not seen before
    ```

### Algorithm 2: Breadth First with all available valid moves and without useful move check

#### Description

- ##### Selection Process
    - Take the first board state from queue.
    - Check if the path for Carter is free to finish the game and make this move if so.
    - All available valid moves are collected and stored in a list of tuples.
    - For every available valid move found, save the new state if not seen before.

- ##### Implementation

    ```pseudocode
    while queue is not empty and no finish is found:
        pop first board state from queue
        check if finish is reached
        move carter if this finishes the game
        else:
            for every available valid move:
                create child and save in queue if child is not seen before
    ```

### Algorithm 3: Breadth First with max steps and with useful move check

#### Description

- ##### Selection Process
    - Take the first board state from queue.
    - Check if the path for Carter is free to finish the game and make this move if so.
    - All maximum moves are collected and stored in a list of tuples.
    - For every useful maximum move found, save the new state if not seen before.

- ##### Implementation

    ```pseudocode
    while queue is not empty and no finish is found:
        pop first board state from queue
        check if finish is reached
        move carter if this finishes the game
        else:
            for every useful max move:
                create child and save in queue if child is not seen before
    ```

### Algorithm 4: Breadth First with all available valid moves and with useful move check

#### Description

- ##### Selection Process

    - Take the first board state from queue.
    - Check if the path for Carter is free to finish the game and make this move if so.
    - All available valid moves are collected and stored in a list of tuples.
    - For every useful available move found, save the new state if not seen before.

- ##### Implementation

    ```pseudocode
    while queue is not empty and no finish is found:
        pop first board state from queue
        check if finish is reached
        move carter if this finishes the game
        else:
            for every useful available move:
                create child and save in queue if child is not seen before
    ```

---

## Step Refiner

### Description

- ##### Parameters
    - Bin size: the specified number of steps used to rewind the board
    - Requires a solved board and its corresponding solved moves

- ##### Implementation

    ```pseudocode
    create list of rewind moves
    while list of rewind moves is not empty:
        create new board state by rewinding specified amount of moves
        run breadth first till old board state is found and save breadth first moves
    ```

---

## Depth First

#### Description

- ##### Selection Process
    - Take the last board state from queue.
    - All available valid moves are collected and stored in a list of tuples.
    - For every available valid move found, save the new state if not seen before.

- ##### Implementation

    ```pseudocode
    while stack is not empty:
        pop last board state from stack
        check if board is solved
            for every available valid move:
                create child and save in stack if child is not seen before
    ```



