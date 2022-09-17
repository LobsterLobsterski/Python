import math
import time
from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int
    h: float # cost path from current node to end
    g: int  # cost path from start to current node
    # parent: Parent.parent = None
    f: float = 0  # cost path from start to end
    parent: tuple = 0, 0 # holds the index of the parent cell

    def calculate_f(self):
        self.f = self.g + self.h

    def update_g(self, current_node_g):
        self.g = current_node_g + 1


class PF:
    def __init__(self, grid_array):
        self.grid_array = grid_array
        self.start, self.end = self.find_start_and_end()
        self.cell_array = self.initialise_cell_array()
        self.start = self.cell_array[self.start[1]][self.start[0]]
        self.end = self.cell_array[self.end[1]][self.end[0]]

        self.found_path = False

    def is_valid(self, x, y, mod_x, mod_y):
        # checks if the position proposed is one that is within boundaries and is not and obstacle
        new_pos = x+mod_x, y+mod_y
        # print(f'{new_pos=}')
        # print(f'{len(self.grid_array[0])=}')
        # print(f'{len(self.grid_array)=}')
        # print(f'{self.grid_array[new_pos[0]][new_pos[1]]=}')
        # print(f'{new_pos[0] > len(self.grid_array[0])=}')
        # print(f'{new_pos[0] < 0=}')
        # print(f'{new_pos[1] > len(self.grid_array)=}')
        # print(f'{new_pos[1] < 0=}')
        # print(f'{self.grid_array[new_pos[0]][new_pos[1]] == 3=}\n')
        try:
            if new_pos[0] > len(self.grid_array[0]) or new_pos[0] < 0 \
                or new_pos[1] > len(self.grid_array) or new_pos[1] < 0 \
                    or self.grid_array[new_pos[0]][new_pos[1]] == 3:
                return False

            return True
        except IndexError:
            return False


    @staticmethod
    def calculate_h(current_cell, goal):
        # calculates a heuristic value for a certain chosen cell
        # h = round(((current_cell[0] - goal[0])**2 + (current_cell[1] - goal[1])**2)**(1/2))
        return round(((current_cell[0] - goal[0])**2 + (current_cell[1] - goal[1])**2)**(1/2), 1)

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

    def reconstruct_path(self, current_cell):
        path = []
        path_cost = current_cell.g
        # path.append((current_cell.y, current_cell.x))
        while current_cell != self.start:
            path.append((current_cell.parent[1], current_cell.parent[0]))
            current_cell = self.cell_array[current_cell.parent[0]][current_cell.parent[1]]

        # print(f'{path=}')
        # print(f'{path_cost=}')
        path.pop()
        return path, path_cost

    def find_path(self, visualiser):

        self.start.g = 0
        open = [self.start]
        closed = []
        counter = 0

        while len(open) > 0 or not self.found_path:  # while open not empty
            counter += 1
            # looking through all cells in open and choosing the
            # one with the smallest f
            current_cell = min(open, key=lambda cell: cell.f)
            temp = open.copy()
            # print(counter)
            # print(f'{open=}')
            # print(f"{current_cell=}")

            # just here to make sure we delete all occurrences of current_cell
            while current_cell in open:
                open.remove(current_cell)
            closed.append(current_cell)

            # if the current cell is the end
            if (current_cell.x, current_cell.y) == (self.end.x, self.end.y):
                print("found a path")
                return self.reconstruct_path(current_cell)
                self.found_path = True
                break

            # if it isn't
            else:
                index_mods = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # defines in which directions we go
                successors = []
                # initialises the list of successors of the current node
                for mod in index_mods:
                    if self.is_valid(current_cell.x, current_cell.y, mod[0], mod[1]):
                        successors.append(self.cell_array[current_cell.x + mod[0]][current_cell.y + mod[1]])



                # this part is fucked, it adds way too many cells
                # to the open list causing it to swell exponentially
                for successor in successors:
                    if successor in closed:
                        continue

                    successor.update_g(current_cell.g)
                    successor.calculate_f()
                    successor.parent = current_cell.x, current_cell.y

                    if successor not in open and successor not in closed:
                        open.append(successor)
                        continue

                    def loop():
                        # temp = open
                        for cell in temp:
                            if successor.x == cell.x and successor.y == cell.y:
                                if successor.f > cell.f:
                                    return
                                if cell in open or cell in closed:
                                    return
                            open.append(successor)
                            return
                    loop()

        if not self.found_path:
            print('no path')
