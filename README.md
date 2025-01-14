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
            randomise.py
        classes/
            __init__.py
            board.py
            vehicle.py
        __init__.py
        helpers.py
    docs/
        images/
    tests/
        board_test.py
        vehicle_test.py
    main.py
    requirement.txt
    README.md
```

### Directory Breakdown
- **`code/`**: Contains the core implementation of the game
    - **`algorithms/`**: Houses heuristic and randomization algorithms
    - **`classes/`**: Defines the `Board` and `Vehicle` classes and their interactions
    - `helpers.py`: Utility functions to support game logic
- **`docs/`**: Documentation for project planning and algorithmic approaches
- **`tests/`**: Unit tests for core functionality
    - `board_test.py`: Tests for the `Board` class
    - `vehicle_test.py`: Tests for the `Vehicle` class
- **`main.py`**: Entry point for running the game
- **`requirement.txt`**: Python package dependencies
- **`README.md`**: This documentation file

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
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

## Running the Project
1. Navigate to the `<rush_hour_folder_name>`
   ```bash
   cd <rush_hour_folder_name>
    ```
2. Run the main script to start the game:
   ```bash
   python main.py
   ```

## Running the Test Suite
1. Navigate to the `<rush_hour_folder_name>`.
   ```bash
   cd <rush_hour_folder_name>
   ```
2. Run all tests using the `unittest` module:
   ```bash
   python -m unittest discover -s tests -p "*.py" -v
   ```
3. To run a specific test file:
   ```bash
   python -m unittest tests/vehicle_test.py -v
   ```

## Goals
- Implement advanced solving algorithms, including:
  - Naive randomization
  - BFS (Breadth-First Search)
  - DFS (Depth-First Search)
  - A* (A-Star) Search

---

Enjoy solving puzzles with **Rush Hour**!

