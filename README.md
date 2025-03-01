# Rush Hour

## Overview

**Rush Hour** is a Python-based implementation of the classic Rush Hour game, developed as part of a heuristics assignment. The game involves maneuvering vehicles on a grid-based board to clear a path for the red vehicle to exit

![6x6 Gameboard](docs/images/Rushhour6x6_1-gameboard.png)

### Key Features
- Loads game boards from CSV file
- Supports different grid sizes: **6x6**, **9x9**, and **12x12**
- Vehicles of length 2 (cars) and 3 (trucks) with restricted movement (forward or backward only along their orientation)
- Comprehensive game rules implemented in Python
- Algorithms to solve the game with minimal steps
- Supports plotting the game state
- Tracks moves for export to CSV

---

## Project Layout
The project follows a modular structure for scalability and clarity:

```
<rush_hour_root_folder>/
    code/
        algorithms/
            __init__.py
            a_star.py
            breadth_first.py
            depth_first.py
            heuristics.py
            randomise.py
            steprefiner.py
        classes/
            __init__.py
            board.py
            game.py
            mover.py
            plotter.py
            vehicle.py
        __init__.py
        helpers.py
        utils.py
    data/
        experiment/
        input/
            gameboards/
                Rushhour6x6_1.csv
                Rushhour6x6_2.csv
                Rushhour6x6_3.csv
                Rushhour9x9_4.csv
                Rushhour9x9_5.csv
                Rushhour9x9_6.csv
                Rushhour12x12_7.csv
            test_boards/
                Rushhour6x6_advanced_1.csv
                Rushhour6x6_advanced_2.csv
                Rushhour6x6_advanced_3.csv
                Rushhour6x6_expert_1.csv
                Rushhour6x6_expert_2.csv
                Rushhour6x6_expert_3.csv
                Rushhour6x6_test.csv
        output/
    docs/
        baseline/
            images/
            Baseline.md
        images/
        Algorithms.md
        README.md
        Representation.md
        State_space.md
    scripts/
        __init__.py
        a_star_script.py
        breadth_first_script.py
        random_script.py
        steprefiner_script.py
    tests/
        __init__.py
        test_board.py
        test_game.py
        test_plotter.py
        test_vehicle.py
    .editorconfig
    .gitignore
    main.py
    pytest.ini
    README.md
    requirements.txt
```

### Folder and files breakdown

- <rush_hour_root_folder>/
    - **`code/`**: Contains the core implementation of the game
        - **`algorithms/`**: Heuristic and randomization algorithms
            - `__init__.py`
            - `a_star.py`: Implements a A* algorithm for solving the game
            - `breadth_first.py`: Implements a Breadth First Search (BFS) algorithm for solving the game
            - `depth_first.py`: Implements a Depth First Search (DFS) algorithm for solving the game
            - `heuristics.py`: Implements some additional heuristics for solving the game
            - `randomise.py`: Implements randomization algorithms for solving the game
            - `steprefiner.py`: Implements 'step refiner' heuristics for solving the game
        - **`classes/`**: Representations of the core objects
            - `__init__.py`
            - `game.py`: Manages gameplay, board setup, moves
            - `board.py`: Represents the game board and manages vehicle placements and moves
            - `mover.py`: Handles rules and move validations
            - `plotter.py`: Handles visualization (static/animated)
            - `vehicle.py`: Represents vehicles, tracking their attributes and movements
        - `__init__.py`
        - `helpers.py`: Helper functions to support finding paths
        - `utils.py`: Utility functions to support writing and reading from files
      - **`data/`**: Data folder for ingesting game boards and storing solutions
        - **`experiment/`**: Contains the results of the experiments
        - **`input/`**: Contains game boards to ingest
            - **`gameboards/`**: Contains 7 game boards to solve
            - **`test_boards/`**: Contains game boards used for testing our algorithms and representation
        - **`output/`**: Folder for storing game solutions and exporting game state visualization
    - **`docs/`**: Documentation for the project's design, planning and results
        - **`baseline/`**: Contains data and images related to the results of randomization algorithms
            - `images/`: Visualizations of baseline measurement results
            - `Baseline.md`: Documents the baseline results and statistical insights
        - **`images/`**: Images used in the various documents
        - `Algorithms.md`: Explains the solving algorithms implemented in the project
        - `Representation.md`: Details the representation choices for modeling the game
        - `README.md`: Overview of the documentation folder and its purpose
        - `State_space.md`: Shows the calculations for the state space sizes for each board
    - **`scripts/`**: Scripts to run experiments with the algorithms
        - `__init__.py`
        - `a_star_script.py`: Runs the A* algorithm
        - `breadth_first_script.py`: Runs the BFS algorithm
        - `random_script.py`: Runs the Random algorithm
        - `steprefiner_script.py`: Runs the Step Refiner algorithm
    - **`tests/`**: Unit tests for ensuring the correctness of core functionality
        - `__init__.py`
        - `test_board.py`: Tests for the `Board` class
        - `test_game.py`: Tests for the `Game` class
        - `test_plotter.py`: Tests for the `Plotter` class
        - `test_vehicle.py`: Tests for the `Vehicle` class
    - `.editorconfig`: Defines consistent coding styles across different editors
    - `.gitignore`: Specifies files and directories to intentionally ignore by `git`
    - `main.py`: Entry point for running the code
    - `pytest.ini`: Config file for PyTest
    - `README.md`: This documentation file
    - `requirements.txt`: Lists Python package dependencies

---

## Additional documentation:
- [Docs](docs)
  - [Representation](docs/Representation.md)
  - [Algorithms](docs/Algorithms.md)
  - [Baseline measurements](docs/Baseline/Baseline.md)
  - [State space](docs/State_space.md)
  - [Heuristics](docs/Heuristics.md)

---

## Setup and Installation

### Prerequisites
- Python 3.10 or later

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/MinAiSpaces/rushhour.git <rush_hour_root_folder>
   cd <rush_hour_folder_name>
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv rushhour
   source rushhour/bin/activate    # On Windows: rushhour\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

#### NB
Generating animations of the moves using `ffmpeg` as `writer` will only work if ffmpeg is installed on the machine. `Pillow` should work as long as `Matplotlib` gets installed (which should be installed if you follow the steps above)

## Running the Project
1. Navigate to the `<rush_hour_folder_name>`:
   ```bash
   cd <rush_hour_folder_name>
    ```

2. Run the main script to start the game:
   ```bash
   python main.py
   ```

## Running the Test Suite
1. Navigate to the `<rush_hour_folder_name>`:
   ```bash
   cd <rush_hour_folder_name>
   ```

2. Run all tests:
   ```bash
   pytest
   ```

3. To run a specific test file:
   ```bash
   pytest tests/vehicle_test.py
   ```

4. To show verbose test results add the `-v` flag:
   ```bash
   pytest -v
   ```

   ```bash
   pytest -v tests/test_vehicle.py
   ```
5. Show test coverage
    ```bash
    pytest --cov
    ```

## Goals
- Implement advanced solving algorithms, including:
  - Naive randomization
  - BFS (Breadth-First Search)
  - DFS (Depth-First Search)
  - A* (A-Star) Search
  - Step Refiner
  - Some additional heuristics

---

## Scripts

The scripts can be found in the **`scripts`** folder and are determined to be used for experiments with the algorithms. Each algorithm has its own script. The experiments are set to run iterations of the chosen algorithm for 3600 seconds. After the set time, the results (number of moves made, solving time, total number of seen states, max queue size, number of unique seen states) of each iteration are written to the **`data/experiment`** folder.

### Running the scripts:
1. Navigate to the `<rush_hour_folder_name>`:
   ```bash
   cd <rush_hour_folder_name>
   ```
2. Run:
   ```bash
   python -m scripts.<script_name> <script_arguments>
   ```


### Random:
- Run:
    ```bash
    python -m scripts.random_script <filename>
    ```
- Example:
    ```bash
    python -m scripts.random_script 'RushHour6x6_1.csv'
    ```

### A*:
- Run:
    ```bash
    python -m scripts.a_star_script <filename>
    ```

- Example:
    ```bash
    python -m scripts.a_star_script 'RushHour6x6_1.csv'
    ```

Optional arguments:
- `-nmm`
    - Boolean flag to disable max moves

---

### BFS:
- Run:
    ```bash
    python -m scripts.breadth_first_script <filename>
    ```

- Example:
    ```bash
    python -m scripts.breadth_first_script 'RushHour6x6_1.csv'
    ```

Optional arguments:
- `-nmm`
    - Boolean flag to disable max moves
- `-um`
    - Boolean flag to enable only useful moves

---

### Step Refiner:
- Run
    ```bash
    python -m scripts.steprefiner_script <filename>
    ```

- Example:
    ```bash
    python -m scripts.steprefiner_script 'RushHour6x6_1'
    ```

Optional arguments:
- `-bz` `<number>`
    - Specify the rewind steps (default: 10)

---

Step Refiner needs a solved game, which we get from running the random script for 1800 seconds.

---

Enjoy solving puzzles with **Rush Hour**!
