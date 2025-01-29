# Heuristics

## Free Carter

### Description

- Checks if the path for Carter is free to end the game. Returns the steps if Carter can reach the finish, else it returns None.

### Implementation

```pseudocode
get max forward steps of carter
if carter can reach the board border:
    return max forward steps
```

## All max moves

### Description

- Returns only the moves with the largest possible steps for all vehicles on the board as a list of moves.

### Implementation

```pseudocode
for every vehicle:
    get max forward and backward steps
    save if steps > 0
return all saved moves
```

## Check useful move

### Description

- Checks for changes to the available valid moves after the move of specified vehicle. Returns True if changes are found.

### Implementation

```pseudocode
save old all available valid moves
move vehicle
save new all available valid moves
if found moves changed between new and old, excluding the moved vehicle:
    return True
else:
    return False
```