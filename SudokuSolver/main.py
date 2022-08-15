#############################################
# Code copied from Kylie Ying with a couple
# adjustments of my own.
# Doing this after trying my own sudoku solver
# was really eye-opening, and i literally
# laughed out loud when it solved the puzzle.
#############################################

def find_next_empty(puzzle):
    # finds next coordinate (row, col) which is empty
    # if the board is filled the it returns (None, None)
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c

    return None, None


def is_valid(puzzle, guess, row, col):
    # figues whether the guess is valid

    # if in row
    if guess in puzzle[row]:
        return False
    # if in col
    if guess in [r[col] for r in puzzle]:
        return False

    # if in block
    # finds starting coord of the block then takes the first, second and third row of the
    # block then for each of the rows it takes the next three col values. At the end
    # it merges them together into one list
    row_start = (row //3) *3
    col_start = (col //3) *3
    block = [*puzzle[row_start][col_start:col_start + 3], *puzzle[row_start + 1][col_start:col_start + 3], *puzzle[row_start + 2][col_start:col_start + 3]]
    if guess in block:
        return False

    return True


def sudoku_solver(puzzle):
    # solving a sudoku using a backtracking algorythm
    # STEP 1: choose a spot to start with
    row, col = find_next_empty(puzzle)

    if row is None:
        return True

    # STEP 2: get a guess and place it in the spot
    for guess in range(1, 10):
        # STEP 3: check if the guess is valid
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            # STEP 4: recurse
            if sudoku_solver(puzzle):
                return True

        # STEP 5: if no valid guess or the guess doesn't solve the puzzle we
        # need to backtrack
        puzzle[row][col] = -1

    # STEP 6: if we're here then we tried every combination possible and none worked
    # that means its unsolvable
    return False


if __name__ == '__main__':
    puzzle = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]
    print(sudoku_solver(puzzle))
    for row in puzzle:
        print(row)
