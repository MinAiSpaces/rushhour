# Algorithms

## Randomization

### Algorithm 1: Uniform randomization of all available valid moves

### Description

- #### Selection Process

    - Before making a move, all available moves are collected and stored in a list of tuples.
    - A move is then selected at random from this list of all available valid moves.

- #### Implementation

```python
while not board.check_game_finished():
    vehicle, steps = random.choice(board.check_available_moves())
    board.move_vehicle(vehicle, steps)
```

## Algorithm 2: Randomization vehicle first

### Description

- #### Selection Process

    - Before making a move, all available moves are collected and stored in a list of tuples.
    - From the list of available valid moves, the unique vehicles are extracted.
    - A vehicle is then selected at random from this list of vehicles.
    - Finally, a valid move for this vehicle is selected at random from the list of available valid moves for this vehicle.

- ### Implementation

```python
while not board.check_game_finished():
    vehicle_moves = {}

    for vehicle, steps in board.check_available_moves():
        vehicle_moves.setdefault(vehicle, []).append(steps)

    random_vehicle = random.choice(list(vehicle_moves.keys()))
    steps = random.choice(vehicle_moves[random_vehicle])

    board.move_vehicle(random_vehicle, steps)
```
