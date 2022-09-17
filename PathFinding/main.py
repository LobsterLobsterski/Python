import sys
import time

import pygame as pg
from ProceduralGeneration import PG
from PathFinding import PF


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

            if colour:
                coords = row_idx*square[1], col_idx*square[0]
                pg.draw.rect(window, colour, (coords[1], coords[0], square[0], square[1]))


def round_to_nearest_square(coords, square):
    # returns the index of the square pressed
    # print(coords)
    # print(square)
    # print((coords[0]//square[0], coords[1]//square[1]))
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


def main():
    # setting the window
    pg.init()
    size = width, height = 500, 500
    dim = rows, cols = 6, 6
    square = width//cols, height//rows
    window = pg.display.set_mode(size)
    pg.display.set_caption("PGaPF")

    # init
    grid_array = [[0 for _ in range(cols)] for _ in range(rows)]
    path = []
    visualiser = False

    # main loop
    while True:
        pressed = False
        square_clicked = -1, -1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    path = []
                    pressed = True
                    start = time.time()
                    pf = PF(grid_array)
                    try:
                        path, path_cost = pf.find_path(visualiser)
                    except (ValueError, TypeError):
                        return
                    print(f'execution time is: {time.time() - start}')
                    print(f'{path=}')
                    print(f'{path_cost=}')

                if event.key == pg.K_r:
                    grid_array = [[0 for _ in range(cols)] for _ in range(rows)]
                    path = []

                if event.key == pg.K_SPACE:
                    path = []
                    pressed = True

            if event.type == pg.MOUSEBUTTONDOWN:
                square_clicked = round_to_nearest_square(pg.mouse.get_pos(), square)

                # when left mouse button is clicked we add a square
                if pg.mouse.get_pressed()[0]:
                    grid_array = set_square_state(grid_array, square_clicked, 0)
                # when the right is pressed we remove a square
                elif pg.mouse.get_pressed()[2]:
                    grid_array = set_square_state(grid_array, square_clicked, 1)

        window.fill((100, 100, 100))
        place_dots(window, grid_array, square)
        grid_array = add_path(grid_array, path, pressed)
        make_grid(window, size, dim, square)
        pg.display.update()


if __name__ == '__main__':
    main()
    pg.quit()
