import math

############################################
# 'code' made by Tomasz Potoczko
# nearly works, i cannot be bothered to waste
# any more time on this stubborn project of
# mine, so i've decided to leave it.
# PEACE
############################################

from puzzle import Puzzle


class Sudoku:
    def __init__(self, puzzle):
        self.puzzle = puzzle  # object of Puzzle class needed for calling on methods
        self.board = [
            [3, 9, 0,   0, 5, 0,   0, 0, 0],
            [0, 0, 0,   2, 0, 0,   0, 0, 5],
            [0, 0, 0,   7, 1, 9,   0, 8, 0],

            [0, 5, 0,   0, 6, 8,   0, 0, 0],
            [2, 0, 6,   0, 0, 3,   0, 0, 0],
            [0, 0, 0,   0, 0, 0,   0, 0, 4],

            [5, 0, 0,   0, 0, 0,   0, 0, 0],
            [6, 7, 0,   1, 0, 5,   0, 4, 0],
            [1, 0, 9,   0, 0, 0,   2, 0, 0]
        ]

        self.number_counter = self.count_numbers()
        self.allowed_nums = set([x for x in range(1, 10)])
        self.pencil = [[None for _ in range(self.puzzle.board_dim)] for _ in range(self.puzzle.board_dim)]
        # self.board = puzzle.puzzle  # the 2d list of sudoku
        self.all_available_nums_rows = []
        self.all_available_nums_cols = []
        self.all_available_nums_nonets = []
        self.weight_array = []

    def count_numbers(self):
        counter = [0 for _ in range(self.puzzle.board_dim)]
        for row in self.board:
            for val in row:
                if val > 0:
                    counter[val-1] += 1

        return counter

    def check_number_counter(self):
        list_of_allowed_nums = [x for x in range(1, 10)]
        for idx, tally in enumerate(self.number_counter):
            if tally > 8:
                # if there is a tally which equals 9 then we have all
                # of the certain value on the board and as such we can
                # remove all of them from the availability arrays
                print(f" it is the end of number {idx+1} as there are now {tally} of them on the board")
                list_of_allowed_nums.remove(idx+1)
        self.allowed_nums = set(list_of_allowed_nums)
        print(f"updated counter: {self.number_counter}")
        print(f"list of allowed numbers: {self.allowed_nums}")

    def print_board(self):
        for row in self.board:
            print(row)

    def all_available_values(self):
        return self.all_available_values_rows(), self.all_available_values_cols(), self.all_available_values_nonets()

    def all_available_values_rows(self):
        all_available_nums = [[0 for _ in range(self.puzzle.board_dim)] for _ in range(self.puzzle.board_dim)]
        for row_idx, row in enumerate(self.board):
            available_nums = [i for i in self.allowed_nums]
            # print(f"available_nums {available_nums}")
            # print(f"row {row}")
            for val in row:
                if val in available_nums:
                    # print(f"idx: {val_idx}")
                    available_nums.remove(val)
            # print(f"available_nums after {available_nums}")
            all_available_nums[row_idx] = available_nums

        # print(f"all_available_nums: {all_available_nums}")
        return all_available_nums

    def all_available_values_cols(self):
        all_available_nums = [[0 for _ in range(9)] for _ in range(9)]
        for col_idx in range(self.puzzle.board_dim):
            column = self.puzzle.get_col(self.board, col_idx)
            available_nums = [i for i in self.allowed_nums]
            # print(f"available_nums {available_nums}")
            # print(f"col {column}")
            for val in column:
                if val in available_nums:
                    # print(f"idx: {val_idx}")
                    available_nums.remove(val)
            # print(f"available_nums after {available_nums}")
            all_available_nums[col_idx] = available_nums

        #print(f"all_available_nums: {all_available_nums}")
        return all_available_nums

    def all_available_values_nonets(self):
        all_available_nums = [[0 for _ in range(9)] for _ in range(9)]
        override_idx = 0  # index under which available moves will be saved
        for nonet_row_idx in range(int(self.puzzle.board_dim**(1/2))):
            for nonet_col_idx in range(int(self.puzzle.board_dim**(1/2))):
                available_nums = [i for i in self.allowed_nums]
                # print(f"row: {nonet_row_idx} col: {nonet_col_idx}")
                nonet = self.puzzle.get_nonet(self.board, nonet_row_idx * 3, nonet_col_idx * 3)
                # print(f"available_nums {available_nums}")
                # print(f"nonet {nonet}")
                for val in nonet:
                    if val in available_nums:
                        # print(f"idx: {val_idx}")
                        available_nums.remove(val)
                # print(f"available_nums after {available_nums}")
                all_available_nums[override_idx] = available_nums
                override_idx += 1

        # print(f"all_available_nums: {all_available_nums}")

        # NOTE FOR SELF:
        # returns nonets left to right from top to down
        return all_available_nums

    def update_availability_arrays(self):
        self.all_available_nums_rows, self.all_available_nums_cols, self.all_available_nums_nonets = self.all_available_values()
        # print("AVAILABILITY ARRAYS UPDATED")

    def get_weight(self, row_idx, col_idx):
        row = self.all_available_nums_rows[row_idx].copy()
        col = self.all_available_nums_cols[col_idx].copy()
        nonet = self.all_available_nums_nonets[self.puzzle.get_nonet(self.board, row_idx, col_idx, True)].copy()

        # print(f"ROW: {row}")
        # print(f"COL: {col}")
        # print(f"nonet: {nonet}")

        shared_values = list(set(row) & set(col) & set(nonet))

        return shared_values

    def add_element(self, element, row_idx, col_idx):
        print(f"adding {element} to {row_idx}, {col_idx}")
        self.board[row_idx][col_idx] = element
        # print("RESETTING NUMBER COUNTER")
        self.number_counter = self.count_numbers()
        self.check_number_counter()
        self.update_availability_arrays()  # the board has changed so we need to change the arrays
        # print("RERUNNING SET_WEIGHTS 1")
        self.set_weights()  # the board has changed and the previous weights may be invalid
        # self.sudoku_solver()

    @staticmethod
    def find_matching(row, col, nonet):
        # print("\nFIND MATCHING")
        array_of_pairs = []
        # print(f"row:  {row}")
        for idx, moves in enumerate(row):
            # this ensures we only get the values which repeat 2 times for 2 values, 3 times for 3 etc.
            # print(f"moves: {moves[1]}")
            counter = 0
            for x in row:
                # print(f"x[1]: {x[1]} == moves[1]: {moves[1]}")
                if x[1] == moves[1]:
                    counter += 1
            # print(f"counter: {counter}")
            if counter > len(moves[1])-1 and moves[1] not in array_of_pairs:
                print(f"THERE IS A PAIR OF {moves[1]} IN THE ROW len: {len(moves[1])}")
                array_of_pairs.append(moves[1])

        # print(f"col:  {col}")
        for idx, moves in enumerate(col):
            # print(f"moves: {moves[1]}")
            counter = 0
            for x in col:
                # print(f"x[1]: {x[1]} == moves[1]: {moves[1]}")
                if x[1] == moves[1]:
                    counter += 1
            # print(f"counter: {counter}")
            if counter > len(moves[1])-1 and moves[1] not in array_of_pairs:
                print(f"THERE IS A PAIR OF {moves[1]} IN THE COL len: {len(moves[1])}")
                array_of_pairs.append(moves[1])

        # print(f"nonet:  {nonet}")
        for idx, moves in enumerate(nonet):
            # print(f"moves: {moves} this many {nonet.count(moves)} and len(moves[1])-1: {len(moves[1])-1}")
            counter = 0
            for x in nonet:
                # print(f"x[1]: {x[1]} == moves[1]: {moves[1]}")
                if x[1] == moves[1]:
                    counter += 1
            # print(f"counter: {counter}")
            if counter > len(moves[1])-1 and moves[1] not in array_of_pairs:
                print(f"THERE IS A PAIR OF {moves[1]} IN THE NONET len: {len(moves[1])}")
                array_of_pairs.append(moves[1])

        print(f"array_of_pairs: {array_of_pairs}")

        return array_of_pairs

    def get_lists_to_check(self, row_idx, col_idx):
        # row = list(filter(lambda spot: spot is not None, self.puzzle.get_row(self.pencil, row_idx)))
        # col = list(filter(lambda spot: spot is not None, self.puzzle.get_col(self.pencil, col_idx)))
        # nonet = list(filter(lambda spot: spot is not None, self.puzzle.get_nonet(self.pencil, row_idx, col_idx)))
        row = []
        for idx, val in enumerate(self.puzzle.get_row(self.pencil, row_idx)):
            if val:
                row.append(((row_idx, idx), val))

        col = []
        for r_idx, roww in enumerate(self.pencil):
            if roww[col_idx]:
                col.append(((r_idx, col_idx), roww[col_idx]))

        nonet = []
        r_idx = math.floor(row_idx / 3) * 3
        c_idx = math.floor(col_idx / 3) * 3
        for r in range(3):
            for c in range(3):
                if self.pencil[r_idx+r][c_idx+c]:
                    nonet.append(((r, c), self.pencil[r_idx+r][c_idx+c]))

        # print(f"row:\n{row}\ncol:\n{col}\nnonet:\n{nonet}")
        # print(f"all together:\n{[*[row], *[col], *[nonet]]}")

        return [*[row], *[col], *[nonet]]

    def find_unique(self):
        # we need to get all the free spots of the row, col and nonet
        # that the spot in row_idx, col_idx is in
        # then we need to find the unique one amongst them
        # print("ALL VIABLE MOVES [pencil]")
        # for x in self.pencil:
        #     print(x)
        # print("NEXT")
        for row_idx, row in enumerate(self.pencil):
            for moves_idx, moves in enumerate(row):
                if self.puzzle.get_row(self.pencil, row_idx)[moves_idx]:
                    print(f"\nCHECKING spot {row_idx}, {moves_idx}")
                    print(f"movs: {self.puzzle.get_row(self.pencil, row_idx)[moves_idx]}")

                    lists_to_check = self.get_lists_to_check(row_idx, moves_idx)
                    # print("lists_to_check")
                    # print(lists_to_check)
                    # print(lists_to_check[0])  # row
                    # print(lists_to_check[0][1]) # tuple containing tuple of coords and list of vals
                    # print(lists_to_check[0][1][1]) # list of values
                    # print(f"row: {lists_to_check[0]}")
                    # print(f"col: {lists_to_check[1]}")
                    # print(f"nonet: {lists_to_check[2]}")
                    print(f"\nCHECKING spot {row_idx}, {moves_idx}")
                    pairs = self.find_matching(lists_to_check[0], lists_to_check[1], lists_to_check[2])
                    # print(f"pairs: {pairs}")
                    # print("\nPENCIL")
                    # for part in self.pencil:
                    #     print(part)
                    # print("\n")
                    print("pencil 1")
                    for r in self.pencil:
                        print(r)
                    print("board 1")
                    self.print_board()
                    ###############################################################################################
                    ### THE PROGRAM IS STILL CHOOSING INCORECT SPOTS AS SUCH AT THE END WE ARE LEST WITH A COUPLE
                    ### OF INFILLABLE SPOTS, WE NEED TO GO THROUGH IT STEP BY STEP AND CHECK WHERE ITS PLACING,
                    ### WHY AND IF ITS CORRECT, THEN WE NEED TO CORRECT IT HAVE FUN FUTURE ME :)
                    ###############################################################################################
                    while pairs:
                        print("pencil 2")
                        for r in self.pencil:
                            print(r)
                        print("board 2")
                        self.print_board()
                        added = False
                        index = ()
                        lists_to_check = self.get_lists_to_check(row_idx, moves_idx)
                        pairs = self.find_matching(lists_to_check[0], lists_to_check[1], lists_to_check[2])
                        for part in lists_to_check:  # part is the row, col or nonet vals
                            print(f"\npart {part}")
                            for val in part:
                                for pair in pairs:
                                    # print(f"pair {pair}")
                                    for pair_val in pair:
                                            print(f"val: {val}\nval[1]: {val[1]}\npair_val: {pair_val}")

                                            if pair == val[1]:
                                                # print("skipped")
                                                continue
                                            if pair_val in val[1]:
                                                print("ITS DERE")
                                                val[1].remove(pair_val)
                                                print(f"new val[1]: {val[1]}")
                                                # time.sleep(2)
                                                if len(val[1]) == 1:
                                                    if self.board[val[0][0]][val[0][1]] == 0:
                                                        self.add_element(val[1][0], val[0][0], val[0][1])
                                                        added = True
                                                        break
                                    if added:
                                        break
                                if added:
                                    break
                            if added:
                                break
                        if not added:
                            print("not added anything in this iteration")
                            break
                    #

                    # print(f"lists of values we need to check for uniqueness: \n{lists_to_check}")
                    # print(f"moves: {moves} for {row_idx}, {moves_idx}")
                    # print(f"get_row of pencil {self.puzzle.get_row(self.pencil, row_idx)[moves_idx]}")
                    for mov in self.puzzle.get_row(self.pencil, row_idx)[moves_idx]:  # its this instead of moves as it changes
                        # print(f"move: {mov}")
                        for part in range(len(lists_to_check)):
                            # print(f"part: {lists_to_check[part]}")
                            # print("next part")
                            counter = 0
                            for array in lists_to_check[part]:
                                # print(f"array: {array[1]}")
                                if mov in array[1]:
                                    # print(f"-------there is a {move} in the {array}")
                                    counter += 1
                                    # print(f"counter: {counter}")
                                # FIX THIS AND MAKE IT PROPER CUZ IT PISSES ME OFF
                                # if counter > 1:
                                #     continue

                            # print(f"counter: {counter}")
                            if counter < 2 and self.board[row_idx][moves_idx] == 0:
                                print(f"##############################################\nFOUND A UNIQUE VALUE {mov} AND ADDED IT TO THE BOARD at {row_idx}, {moves_idx}\n################################3")
                                self.add_element(mov, row_idx, moves_idx)
                                break

    def set_weights(self):
        # print("RERUNNING SET_WEIGHTS 2 AND RESETTING THE PENCIL ARRAY")
        self.pencil = [[None for _ in range(self.puzzle.board_dim)] for _ in range(self.puzzle.board_dim)]
        if self.allowed_nums:
            # print("goes through the initial if")
            # set to math.inf as to make any normal weight_array be able to pass the if statement
            weights = [[math.inf for _ in range(self.puzzle.board_dim)]for _ in range(self.puzzle.board_dim)]
            # lightest = 9
            # lightest_vals = []
            for row_idx, row in enumerate(self.board):
                for col_idx, _ in enumerate(row):
                    if self.board[row_idx][col_idx] != 0:
                        # if it has a value assigned we skip
                        continue

                    # print(f"Row: {row_idx} Col: {col_idx}")
                    viable_vals = self.get_weight(row_idx, col_idx)

                    if len(viable_vals) == 1 and self.board[row_idx][col_idx] == 0:
                        print(f"##############################################\nadded a num with the weight 1 finder algorythm##############################################\n")
                        self.add_element(viable_vals[0], row_idx, col_idx)
                        weights[row_idx][col_idx] = math.inf
                        continue

                    # if len(viable_vals) < lightest:
                    #     lightest = len(viable_vals)
                    #     lightest_vals = viable_vals.copy()
                    #     coord = (row_idx, col_idx)

                    self.pencil[row_idx][col_idx] = viable_vals
                    weights[row_idx][col_idx] = len(viable_vals)

            # print("WEIGHTS")
            # for row in weights:
            #     print(row)
            # print("BOARD")
            # for row in self.board:
            #     print(row)
            return weights
        else:
            print("\n\nWe've done it! The board is filled!\n\n")
            # print("\nWEIGHTS ARRAY")
            # for row in self.weight_array:
            #     print(row)

    def sudoku_solver(self):
        # STEP 1:
        # making a choice depends on three factors:
        #   1. is the value we are considering to put in the
        #       spot we are considering in the row?
        #   2. is the value we are considering to put in the
        #            spot we are considering in the column?
        #   3. is the value we are considering to put in the
        #            spot we are considering in the nonet?
        # STEP 2: WIP
        #   a. loop through the board to find free spots
        #   b. using the arrays of available numbers find
        #       the only available viable numbers to be placed
        #   c. count them and assign to the spot a 'weight_array'
        #       which will be equal to the number of gotten from step b
        #   d. if the weight_array is 1 then there is only 1 viable number
        #       to be placed in the spot, so fill it out and keep on
        #       going through the sudoku until there are no weight_array 1
        #       spots left
        #   e. now we need to consider the spots with possible contradictions and
        #       resolve them by finding contradiction in viable values for other spots
        #       across the rows, cols and nonets. We check if a value is unique across
        #       the three lists meaning that this spot can be the only spot it can be in
        #       as every row, col and nonet needs to contain that number
        #   f. now we need to look for pairs of possible values in paires of spots
        #       (or triplets or quadruplets etc.) because then we can remove these
        #       possible values from all other viable spots they may be in

        print("STARTING PUZZLE")
        self.print_board()

        self.update_availability_arrays()
        # print("\nAVE ARRAYS INITIALISED")

        print(f"\ntally of the values on the board: \n{self.number_counter}")
        sum_of_tally = sum(self.number_counter)

        print("\nINITALISING THE ARRAY OF WEIGHTS AND AS SUCH STARTING THE PROGRAM")
        self.weight_array = self.set_weights()

        print("\nWEIGHTS ARRAY")
        for row in self.weight_array:
            print(row)

        print("\nBOARD AFTER ALL THE INITIAL WEIGHT 1 SPOTS HAVE BEEN FILLED")
        for row in self.board:
            print(row)

        print(F"WE'VE GAINED {sum(self.number_counter) - sum_of_tally} NEW VALUES")
        sum_of_tally = sum(self.number_counter)

        print(f"\ntally of the values on the board: \n{self.number_counter}")

        print("\nSTARTING THE UNIQUE VALUE FINDER ALGORYTHM")
        self.find_unique()

        print("\nBOARD AFTER ALL THE UNIQUE VALUE FINDER ALGORYTHM")
        for row in self.board:
            print(row)

        print(F"WE'VE GAINED {sum(self.number_counter) - sum_of_tally} NEW VALUES")
        sum_of_tally = sum(self.number_counter)

        print(f"\ntally of the values on the board: \n{self.number_counter}")


if __name__ == '__main__':
    grid_size = 9
    num_of_vals = 25
    puzzle = Puzzle(grid_size, num_of_vals) # WILL NEED FIXING WHEN THE MAIN ALGORYTHM IS FULLY FUNCTIONAL
    # puzzle.print_puzzle()
    sudoku = Sudoku(puzzle)
    sudoku.sudoku_solver()

# self.board = [
#             [3, 9, 0,   0, 5, 0,   0, 0, 0],
#             [0, 0, 0,   2, 0, 0,   0, 0, 5],
#             [0, 0, 0,   7, 1, 9,   0, 8, 0],
#
#             [0, 5, 0,   0, 6, 8,   0, 0, 0],
#             [2, 0, 6,   0, 0, 3,   0, 0, 0],
#             [0, 0, 0,   0, 0, 0,   0, 0, 4],
#
#             [5, 0, 0,   0, 0, 0,   0, 0, 0],
#             [6, 7, 0,   1, 0, 5,   0, 4, 0],
#             [1, 0, 9,   0, 0, 0,   2, 0, 0]
#         ]self.board = [
#             [0, 0, 2,   0, 0, 0,   0, 1, 5],
#             [8, 0, 0,   0, 0, 2,   4, 9, 0],
#             [0, 4, 9,   0, 0, 0,   0, 0, 8],
#
#             [0, 1, 0,   0, 0, 0,   6, 0, 0],
#             [7, 0, 3,   9, 0, 0,   0, 0, 0],
#             [9, 2, 0,   0, 6, 0,   0, 4, 0],
#
#             [0, 0, 0,   0, 0, 0,   0, 0, 4],
#             [2, 0, 0,   6, 0, 1,   5, 0, 7],
#             [0, 0, 0,   5, 0, 7,   1, 0, 0]
#         ]

