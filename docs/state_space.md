# State space
## Explanation

For the calculation of the state space of each board we take the product of all possible configurations of every row and column.
To calculate the amount of different configurations for a single row/column we check te amount of vehicle present in that row/colomn and the amount of 'empty' spaces left.

- A vehicle is considered present in the row/column if the entirety of the vehicle is within that row/column.
- A space in the row/column is considered empty if it is not occupied by a vehicle present in that row/column.
- For the vehicles present in the row/column we adhere to the rule that vehicles cannot be placed on top of each other or cross one another.
- For the row where **carter** is present the final space does not count as an 'empty' space since **carter** being there constitutes a finished game.


### Formulas

To calculate the amount of different configurations of a single row/column

for v=0
$$n = 1$$

for v=1:
$$n = s + 1$$

for v=2:
$$n = \sum_{i=0}^{s}1+i$$

for v=3:
$$n = \sum_{j=0}^{s}\sum_{i=0}^{j}1+i$$

for v=4:
$$n = \sum_{k=0}^{s}\sum_{j=0}^{k}\sum_{i=0}^{j}1+i$$

for v=5:
$$n = \sum_{l=0}^{s}\sum_{k=0}^{l}\sum_{j=0}^{k}\sum_{i=0}^{j}1+i$$

- n = amount of different configurations
- v = number of vehicles present
- s = number of empty spaces


### Table

|       |s=0|s=1|s=2 |s=3 |s=4  |s=5  |s=6  |s=7  |s=8   |s=9   |s=10  |s=11  |s=12  |
|-------|---|---|----|----|-----|-----|-----|-----|------|------|------|------|------|
|**v=0**|n=1|n=1|n=1 |n=1 |n=1  |n=1  |n=1  |n=1  |n=1   |n=1   |n=1   |n=1   |n=1   |
|**v=1**|n=1|n=2|n=3 |n=4 |n=5  |n=6  |n=7  |n=8  |n=9   |n=10  |n=11  |n=12  |n=13  |
|**v=2**|n=1|n=3|n=6 |n=10|n=15 |n=21 |n=28 |n=36 |n=45  |n=55  |n=66  |n=78  |n=91  |
|**v=3**|n=1|n=4|n=10|n=20|n=35 |n=56 |n=84 |n=120|n=165 |n=220 |n=286 |n=364 |n=455 |
|**v=4**|n=1|n=5|n=15|n=35|n=70 |n=126|n=210|n=330|n=495 |n=715 |n=1001|n=1365|n=1820|
|**v=5**|n=1|n=6|n=21|n=56|n=126|n=252|n=462|n=792|n=1287|n=2002|n=3003|n=4368|n=6188|


## Boards

### 6x6_1

#### rows/columns

- row 1: v=2, s=1 &rarr; n=3
- row 2: v=2, s=2 &rarr; n=6
- row 3: v=1, s=3 &rarr; n=4
- row 4: v=2, s=2 &rarr; n=6
- row 5: v=1, s=4 &rarr; n=5
- row 6: v=0, s=6 &rarr; n=1
- col 1: v=1, s=4 &rarr; n=5
- col 2: v=0, s=6 &rarr; n=1
- col 3: v=2, s=2 &rarr; n=6
- col 4: v=1, s=4 &rarr; n=5
- col 5: v=0, s=6 &rarr; n=1
- col 6: v=1, s=4 &rarr; n=5

#### statespace
1.62E6


### 6x6_2

#### rows/columns

- row 1: v=2, s=2 &rarr; n=6
- row 2: v=2, s=2 &rarr; n=6
- row 3: v=1, s=3 &rarr; n=4
- row 4: v=2, s=2 &rarr; n=6
- row 5: v=1, s=4 &rarr; n=5
- row 6: v=1, s=4 &rarr; n=5
- col 1: v=1, s=4 &rarr; n=5
- col 2: v=0, s=6 &rarr; n=1
- col 3: v=0, s=6 &rarr; n=1
- col 4: v=1, s=4 &rarr; n=5
- col 5: v=1, s=4 &rarr; n=5
- col 6: v=1, s=3 &rarr; n=4

#### statespace
1.08E7


### 6x6_3

#### rows/columns

- row 1: v=1, s=4 &rarr; n=5
- row 2: v=0, s=6 &rarr; n=1
- row 3: v=1, s=3 &rarr; n=4
- row 4: v=1, s=4 &rarr; n=5
- row 5: v=1, s=4 &rarr; n=5
- row 6: v=1, s=4 &rarr; n=5
- col 1: v=1, s=4 &rarr; n=5
- col 2: v=0, s=6 &rarr; n=1
- col 3: v=1, s=3 &rarr; n=4
- col 4: v=1, s=3 &rarr; n=4
- col 5: v=0, s=6 &rarr; n=1
- col 6: v=1, s=3 &rarr; n=4

#### statespace
8E5


### 9x9_4

#### rows/columns

- row 1: v=1, s=6 &rarr; n=7
- row 2: v=1, s=6 &rarr; n=7
- row 3: v=0, s=9 &rarr; n=1
- row 4: v=2, s=4 &rarr; n=15
- row 5: v=1, s=6 &rarr; n=7
- row 6: v=1, s=6 &rarr; n=7
- row 7: v=2, s=5 &rarr; n=21
- row 8: v=0, s=9 &rarr; n=1
- row 9: v=3, s=2 &rarr; n=10
- col 1: v=3, s=3 &rarr; n=20
- col 2: v=0, s=9 &rarr; n=1
- col 3: v=1, s=6 &rarr; n=7
- col 4: v=3, s=2 &rarr; n=10
- col 5: v=1, s=7 &rarr; n=8
- col 6: v=1, s=6 &rarr; n=7
- col 7: v=0, s=9 &rarr; n=1
- col 8: v=0, s=9 &rarr; n=1
- col 9: v=1, s=4 &rarr; n=10

#### statespace
5.930E12


### 9x9_5

#### rows/columns

- row 1: v=1, s=6 &rarr; n=7
- row 2: v=1, s=7 &rarr; n=8
- row 3: v=1, s=7 &rarr; n=8
- row 4: v=2, s=5 &rarr; n=21
- row 5: v=2, s=3 &rarr; n=10
- row 6: v=0, s=9 &rarr; n=1
- row 7: v=2, s=5 &rarr; n=21
- row 8: v=2, s=4 &rarr; n=15
- row 9: v=1, s=7 &rarr; n=8
- col 1: v=2, s=5 &rarr; n=21
- col 2: v=1, s=7 &rarr; n=8
- col 3: v=1, s=7 &rarr; n=8
- col 4: v=1, s=6 &rarr; n=7
- col 5: v=1, s=7 &rarr; n=8
- col 6: v=2, s=4 &rarr; n=15
- col 7: v=2, s=5 &rarr; n=21
- col 8: v=0, s=9 &rarr; n=1
- col 9: v=2, s=4 &rarr; n=15


#### statespace
8.431E16


### 9x9_6

#### rows/columns

- row 1: v=2, s=5 &rarr; n=21
- row 2: v=2, s=4 &rarr; n=15
- row 3: v=2, s=5 &rarr; n=21
- row 4: v=1, s=6 &rarr; n=7
- row 5: v=1, s=6 &rarr; n=7
- row 6: v=2, s=5 &rarr; n=21
- row 7: v=2, s=4 &rarr; n=15
- row 8: v=2, s=5 &rarr; n=21
- row 9: v=1, s=6 &rarr; n=7
- col 1: v=2, s=4 &rarr; n=15
- col 2: v=1, s=7 &rarr; n=8
- col 3: v=1, s=7 &rarr; n=8
- col 4: v=1, s=6 &rarr; n=7
- col 5: v=3, s=2 &rarr; n=10
- col 6: v=1, s=7 &rarr; n=8
- col 7: v=0, s=9 &rarr; n=1
- col 8: v=1, s=7 &rarr; n=8
- col 9: v=1, s=6 &rarr; n=7

#### statespace
4.519E17


### 12x12_7

#### rows/columns

- row 1: v=2, s=7 &rarr; n=36
- row 2: v=0, s=12 &rarr; n=1
- row 3: v=3, s=5 &rarr; n=56
- row 4: v=2, s=8 &rarr; n=45
- row 5: v=2, s=6 &rarr; n=28
- row 6: v=1, s=9 &rarr; n=10
- row 7: v=2, s=7 &rarr; n=36
- row 8: v=3, s=5 &rarr; n=56
- row 9: v=3, s=4 &rarr; n=35
- row 10: v=2, s=7 &rarr; n=36
- row 11: v=0, s=12 &rarr; n=1
- row 12: v=3, s=5 &rarr; n=56
- col 1: v=2, s=7 &rarr; n=36
- col 2: v=1, s=9 &rarr; n=10
- col 3: v=1, s=10 &rarr; n=11
- col 4: v=1, s=10 &rarr; n=11
- col 5: v=1, s=10 &rarr; n=11
- col 6: v=3, s=6 &rarr; n=84
- col 7: v=4, s=1 &rarr; n=5
- col 8: v=1, s=10 &rarr; n=11
- col 9: v=0, s=12 &rarr; n=1
- col 10: v=2, s=8 &rarr; n=45
- col 11: v=2, s=7 &rarr; n=36
- col 12: v=3, s=6 &rarr; n=84

#### statespace
1.088E30