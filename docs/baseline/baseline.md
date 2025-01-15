For the implementation of the randomise algorithm, we created two implementations of the randomise algorithm. The first implementation looks to all the valid moves on the board. A move is valid when vehicles cannot pass through each other and can only move in their assigned orientation (forward and back).

As the first implementation is dependent on all the valid moves and some vehicles could have a bias for making more valid moves than another vehicles, a second implementation is also introduced. In the second implementation of the randomise algorithm, the algorithm first looks to all the vehicles on the board, in which it chooses a random vehicle and then a valid move for this specific vehicle.

