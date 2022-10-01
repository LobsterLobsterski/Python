import pygame as pg
import time


def make_grid(window, size, dim, square):
    # draws a grid on the screen
    x, y = 0, 0
    for i in range(dim[1]):
        x += square[0]
        pg.draw.line(window, (0, 0, 0), (x, 0), (x, size[1]))

    for i in range(dim[0]):
        y += square[1]
        pg.draw.line(window, (0, 0, 0), (0, y), (size[0], y))


def place_dots(window, grid_array, square):
    # creates coloured rectangles on the screen
    # in places denoted by the grid_array
    for row_idx, row in enumerate(grid_array):
        for col_idx, val in enumerate(row):
            colour = False
            if val == 1:
                colour = 0, 0, 255
            elif val == 2:
                colour = 0, 255, 0
            elif val == 3:
                colour = 255, 0, 0
            elif val == 4:
                colour = 221, 161, 221
            elif val == 5:
                colour = 255, 255, 0

            if colour:
                coords = row_idx*square[1], col_idx*square[0]
                pg.draw.rect(window, colour, (coords[1], coords[0], square[0], square[1]))


def draw_start_end_obstacles(window, grid_array, square):
    for row_idx, row in enumerate(grid_array):
        for col_idx, val in enumerate(row):
            colour = False
            if val == 1:
                colour = 0, 0, 255
                # print('start')
            elif val == 2:
                # print('end')
                colour = 0, 255, 0
            elif val == 3:
                colour = 255, 0, 0

            if colour:
                coords = row_idx*square[1], col_idx*square[0]
                pg.draw.rect(window, colour, (coords[1], coords[0], square[0], square[1]))


def draw_visaliser(window, square, visualiser_list, counter):
    for i in range(counter):
        coords = visualiser_list[i][0]*square[1], visualiser_list[i][1]*square[0]
        pg.draw.rect(window, (255, 255, 0), (coords[0], coords[1], square[0], square[1]))
        if i == counter-1:
            time.sleep(0.05)


def draw_path(window, grid_array, square):
    for row_idx, row in enumerate(grid_array):
        for col_idx, val in enumerate(row):
            colour = False
            if val == 4:
                colour = 221, 161, 221

            if colour:
                coords = row_idx*square[1], col_idx*square[0]
                pg.draw.rect(window, colour, (coords[1], coords[0], square[0], square[1]))


def round_to_nearest_square(coords, square):
    return coords[0]//square[0], coords[1]//square[1]


def set_square_state(grid_array, square, button_pressed):
    # changes the values of grid_array to 1 (start), 2 (end) or 3 (obstacle)
    square = square[1], square[0]  # a quick flip as the grid array was sideways
    start_placed = False
    end_placed = False

    if button_pressed == 0:
        for row in grid_array:
            if 1 in row:
                start_placed = True
            if 2 in row:
                end_placed = True

            if start_placed and end_placed:
                break

        if not start_placed:
            grid_array[square[0]][square[1]] = 1

        elif not end_placed:
            grid_array[square[0]][square[1]] = 2

        else:
            grid_array[square[0]][square[1]] = 3

    else:
        grid_array[square[0]][square[1]] = 0

    return grid_array


def add_path(grid_array, path, pressed):
    if pressed:
        for row_idx, row in enumerate(grid_array):
            for col_idx, val in enumerate(row):
                if val == 4:
                    grid_array[row_idx][col_idx] = 0

    if path:
        for coords in path:
            if grid_array[coords[1]][coords[0]] == 3:
                continue
            grid_array[coords[1]][coords[0]] = 4

    return grid_array
