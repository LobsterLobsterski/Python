import math
import timeit
from dataclasses import dataclass
from minHeap import BinaryHeap


@dataclass
class Cell:
    x: int
    y: int
    h: float  # cost path from current node to end
    g: int  # cost path from start to current node
    f: float = 0  # cost path from start to end
    parent: tuple = 0, 0  # holds the index of the parent cell

    def calculate_f(self):
        self.f = self.g + self.h

    def update_g(self, current_node_g):
        self.g = current_node_g + 1

    def __str__(self):
        return f'Cell({self.x}, {self.y})'

    def __hash__(self):
        return hash(self.f)

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


class PF:
    def __init__(self, grid_array):
        self.grid_array = grid_array
        self.start, self.end = self.find_start_and_end()

        start = timeit.default_timer()
        self.cell_array = self.initialise_cell_array()
        end = timeit.default_timer()
        print(f'cell array init time: {end-start}')

        self.start = self.cell_array[self.start[0]][self.start[1]]
        self.end = self.cell_array[self.end[0]][self.end[1]]
        # print(f'{self.start= }, {self.end= }')

        self.found_path = False

    def is_valid(self, x, y, mod_x, mod_y):
        # checks if the position proposed is one that is within boundaries and is not and obstacle
        new_pos = x+mod_x, y+mod_y
        try:
            if new_pos[0] > len(self.grid_array[0]) or new_pos[0] < 0 \
                or new_pos[1] > len(self.grid_array) or new_pos[1] < 0 \
                    or self.grid_array[new_pos[1]][new_pos[0]] == 3:
                return False

            return True
        except IndexError:
            return False

    @staticmethod
    def calculate_h(current_cell, goal):
        # calculates a heuristic value for a certain chosen cell
        # return round(((current_cell[0] - goal[0])**2 + (current_cell[1] - goal[1])**2)**(1/2), 2)
        return abs(current_cell[0]-goal[0]) + abs(current_cell[1]-current_cell[0])

    def initialise_cell_array(self):
        cell_array = [[0 for _ in range(len(self.grid_array[0]))] for _ in range(len(self.grid_array))]
        for row_idx, row in enumerate(self.grid_array):
            for col_idx, val in enumerate(row):
                cell = Cell(row_idx, col_idx, self.calculate_h((row_idx, col_idx), self.end), 1)
                cell.calculate_f()
                cell_array[row_idx][col_idx] = cell



        return cell_array

    def find_start_and_end(self):
        start = end = 0, 0
        for row_idx, row in enumerate(self.grid_array):
            for col_idx, val in enumerate(row):
                if val == 1:
                    start = col_idx, row_idx
                if val == 2:
                    end = col_idx, row_idx

        return start, end

    def reconstruct_path(self, current_cell, visualiser=[]):
        path = []
        path_cost = current_cell.g
        while current_cell != self.start:
            path.append((current_cell.parent[0], current_cell.parent[1]))
            current_cell = self.cell_array[current_cell.parent[0]][current_cell.parent[1]]

        path.pop()

        if visualiser:
            visualiser.remove((self.start.x, self.start.y))
            visualiser.remove((self.end.x, self.end.y))

        return path, path_cost, visualiser

    def find_path(self, visualiser_on=False):
        # path is fucked,
        # it takes unnecessary detours and takes suboptimal routes
        pf = timeit.default_timer()
        self.start.g = 0
        # open = [self.start]
        open = BinaryHeap()
        open.insert(self.start)
        # open = set()
        # open.add(self.start)
        # print(f'{open.heap}')
        closed = []
        visualiser = []
        counter = 0

        print('while')
        while open:  # while open not empty
            counter += 1
            # looking through all cells in open and choosing the
            # one with the smallest f
            # current_cell = min(open, key=lambda cell: cell.f)
            # current_cell = open.pop()
            # print(counter)
            # print(open.heap)
            current_cell = open.extractMin()
            closed.append(current_cell)

            if visualiser_on:
                visualiser.append((current_cell.x, current_cell.y))


            # print(f"=={current_cell=}")

            # just here to make sure we delete all occurrences of current_cell
            # if current_cell in open:
            #     print('still in')
                # open.decreaseKey()

            # if the current cell is the end
            if current_cell == self.end:
                print("found a path")
                end = timeit.default_timer()
                print(f'pf execution time: {end-pf}')
                if visualiser_on:
                    return self.reconstruct_path(current_cell, visualiser)
                return self.reconstruct_path(current_cell)

            # if it isn't
            else:
                # , (-1, -1), (1, 1), (-1, 1), (-1, 1)
                index_mods = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # defines in which directions we go
                successors = []
                # initialises the list of successors of the current node
                for mod in index_mods:
                    if self.is_valid(current_cell.x, current_cell.y, mod[0], mod[1]):
                        successors.append(self.cell_array[current_cell.x + mod[0]][current_cell.y + mod[1]])

                # to the open list causing it to swell exponentially
                for successor in successors:
                    if successor in closed:
                        continue

                    successor.update_g(current_cell.g)
                    successor.calculate_f()
                    successor.parent = current_cell.x, current_cell.y

                    # print(f'{successor=}')

                    if successor not in open and successor not in closed:
                        # print(f'if not in any of two, successor insert: {successor}')
                        open.insert(successor)
                        continue

                    # if successor in open:
                    #     print(f'successro duplicate: {successor}')

                    # def loop():
                    #     # temp
                    #     for cell in open:
                    #         if successor == cell:
                    #             if successor > cell:
                    #                 return
                    #             if successor in open or successor in closed:
                    #                 return
                    #         print(f'in loop, successor insert: {successor}')
                    #         open.insert(successor)
                    #         return
                    # loop()
                # print(f'{successors=}\n')
