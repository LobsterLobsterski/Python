When I found the sudoku solver idea for a project I wanted to do it on my own and at the start it was preety rewarding doing these little steps which later then worked together.
But now I've hit a wall and the code is so cluttered and scrambled that it is difficult to debug and find faults in its processes. As such, I've decided to give in, cut my loses and do it with a proper algorythm. I was pretty much coding it to solve like a human would, so I was making lists of weights and pencil marks so that the program can check it. I've also tried to make an algorythm which will generate a random sudoku but it failed and i didin't want to spend too much time on it so i scrapped it.

The way it works:
	- Firstly it goes through the sudoku and fills it out with weights (where the weight is the amount of penciled in possible values) and if it finds a weight 1 spot it fills it out with the appropriaate number.
	- Then it checks for values within the pencil array (which holds all the penciled values) and finds a unique value in the row, column and block portions as such a value must be in that spot.
	- Meanwhile it also looks for pairs of values i.e. [3, 6] in 2 spots or [2, 4, 7] in 3 spots in any given row, column or block as this means that the values in pairs can be removed from the row, cloumn and block as they need to be in these spots which frees up the pencil array and allows the previous two functions to fill it out.

Theoretically it works wonders but practically it is a nightmare. It managed to solve an easy puzzle, and if i managed to debug it compeletely it maybe would of finished a medium/hard puzzle but I cannot be bothered with it anymore. 

This project was nonetheless still interesting and useful to a degree.