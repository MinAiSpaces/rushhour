# Baseline measurements

## Setup

We've run the algorithm 10,000 times for each board and each algorithm. Whenever a board was solved, we tracked how many moves it took for the algorithm to find a solution. The number of moves necessary was then stored so that we could perform some basic statistical calculations on them and plot both a distribution graph and a graph of the sorted list of number of moves, showing the difference in the number of moves over 10,000 runs.

## Algorithm 1: Uniform randomization of all available valid moves

### Performance

- #### Test Boards
    - Board 1 (6x6) - 13 vehicles: **5,835.64 moves** (average over 10_000 runs)
    - Board 2 (6x6) - 13 vehicles: **1290.55 moves**
    - Board 3 (6x6) - 9 vehicles: **17,076.55 moves**
    - Board 4 (9x9) - 22 vehicles: **11,477.30 moves**
    - Board 5 (9x9) - 24 vehicles: **21,606.59 moves**
    - Board 6 (9x9) - 26 vehicles: **13,888.05 moves**
    - Board 7 (12x12) - 44 vehicles: **21,478.40 moves**

- #### Findings
![Table 1](images/Baseline_table_all_available_moves.png)

## Algorithm 2: Randomization vehicle first

### Performance

- #### Test Boards
    - Board 1 (6x6) - 13 vehicles: **8,221.35 moves** (average over 10_000 runs)
    - Board 2 (6x6) - 13 vehicles: **1,570.40 moves**
    - Board 3 (6x6) - 9 vehicles: **16,443.25 moves**
    - Board 4 (9x9) - 22 vehicles: **17,447.04 moves**
    - Board 5 (9x9) - 24 vehicles: **24,055.37 moves**
    - Board 6 (9x9) - 26 vehicles: **17,329.71 moves**
    - Board 7 (12x12) - 44 vehicles: **31,64.73 moves**

- #### Findings
![Table 2](images/Baseline_table_vehicle_first.png)


## Overall observations

First observation was that the random algorithms used were able to solve all games.

Secondly, we've observed that randomization algorithm `Algorithm 1` performed better on all boards except for `Board 3 (6x6)`.

Further we've observed that the distribution of necessary number of moves per board are all right skewed.

And finally we've observed the extreme range of moves made by the algorithms on `Board 6`.

![Table 3](images/Baseline_table_relative_difference.png)

## Analysis

First observation means that all games are solvable.

The fact that `Algorithm 1` is overall better could mean that vehicles with more available moves are more important in finding the correct solution.

The right skewness could be explained by the fact that the algorithm can get stuck in a loop or in a funnel, where there is only a small possibility to escape from.

The large range could be explained by the before mentioned.

## Figures

### Board 1 - algorithm 1
![Figure 1](images/RushHour6x6_1_baseline_all_available.png)

### Board 1 - algorithm 2
![Figure 2](images/RushHour6x6_1_baseline_vehicle_first.png)

### Board 2 - algorithm 1
![Figure 3](images/RushHour6x6_2_baseline_all_available.png)

### Board 2 - algorithm 2
![Figure 4](images/RushHour6x6_2_baseline_vehicle_first.png)

### Board 3 - algorithm 1
![Figure 5](images/RushHour6x6_3_baseline_all_available.png)

### Board 3 - algorithm 2
![Figure 6](images/RushHour6x6_3_baseline_vehicle_first.png)

### Board 4 - algorithm 1
![Figure 7](images/RushHour9x9_4_baseline_all_available.png)

### Board 4 - algorithm 2
![Figure 8](images/RushHour9x9_4_baseline_vehicle_first.png)

### Board 5 - algorithm 1
![Figure 9](images/RushHour9x9_5_baseline_all_available.png)

### Board 5 - algorithm 2
![Figure 10](images/RushHour9x9_5_baseline_vehicle_first.png)

### Board 6 - algorithm 1
![Figure 11](images/RushHour9x9_6_baseline_all_available.png)

### Board 6 - algorithm 2
![Figure 12](images/RushHour9x9_6_baseline_vehicle_first.png)

### Board 7 - algorithm 1
![Figure 11](images/RushHour12x12_7_baseline_all_available.png)

### Board 7 - algorithm 2
![Figure 11](images/RushHour12x12_7_baseline_vehicle_first.png)
