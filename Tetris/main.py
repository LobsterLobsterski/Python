import sys
import pygame as pg
import random
from shape import Shape


def stain(grid_array, tetrino):
    # this method will 'stain' the grid with all the tetrinos which have reached the bottom
    print(tetrino.shape)
    print(len(tetrino.shape))
    counter = 0
    average_x = 0
    average_y = 0
    for coordinates in tetrino.shape:
        x, y = coordinates[0]//30, coordinates[1]//30
        # print(f"x:{x} y:{y}")
        if counter < 3:
            counter += 1
            average_x += x
            average_y += y
        elif counter == 3:
            average_x = (average_x + x) // 4
            average_y = (average_y + y) // 4
            print(f"average_x:{average_x}, average_y:{average_y}")
            counter = 0
            average_x, average_y = 0, 0
    return grid_array


def get_rand_shape():
    rand_shape = random.choice(["I", "J", "L", "O", "S", "T", "Z"])
    print(rand_shape)
    return Shape(rand_shape)


def make_grid(window, width, height, rows, cols):
    # draws a grid on the screen
    distance_btw_rows = width//rows
    distance_btw_cols = height//cols
    x, y = 0, 0
    for i in range(rows):
        x += distance_btw_rows
        pg.draw.line(window, (0, 0, 0), (x, 0), (x, height))

    for i in range(cols):
        y += distance_btw_cols
        pg.draw.line(window, (0, 0, 0), (0, y), (width, y))


def make_shape(window, dx, dy, tetrino):
    tetrino.make_shape(dx, dy)
    pg.draw.polygon(window, tetrino.colour, tetrino.shape)


def rotate(window, tetrino):
    tetrino.rotate(270)
    pg.draw.polygon(window, tetrino.colour, tetrino.shape)

def main():
    # setting the window
    pg.init()
    size = width, height = 300, 600
    rows, cols = 10, 20
    window = pg.display.set_mode(size)
    pg.display.set_caption("TETRIS")

    # setting the fps
    clock = pg.time.Clock()
    clock.tick(60)

    # game initialisation
    grid_array = [[0 for _ in range(rows)] for _ in range(cols)]
    square = 30  # used to denote the distance
    counter = 0  # used for counting frames
    current_shape = get_rand_shape()
    next_shape = get_rand_shape()
    # game loop
    while 1:
        dx, dy = 0, 0
        for event in pg.event.get():
            if event.type == pg.USEREVENT:
                print(event)
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    dx += square
                if event.key == pg.K_LEFT:
                    dx -= square
                if event.key == pg.K_DOWN:
                    dy += square
                if event.key == pg.K_UP:
                    # ROTATE
                    print(F"current_shape.shape before\n{current_shape.shape}")
                    current_shape.rotate(90)
                    print(F"current_shape.shape after\n{current_shape.shape}")

        # making sure we don't step over the window
        if current_shape.x < 0 or current_shape.x > width-square:
            current_shape.x = 0 if current_shape.x < 0 else width-square

        if current_shape.y > height-current_shape.height:
            # get new shape object and set it to the controlled on
            # grid_array = stain(grid_array, current_shape)
            current_shape = next_shape
            next_shape = get_rand_shape()
            current_shape.x, current_shape.y = 4*square, 0

        # every second the shape will drop by one square
        if counter > 1000:
            counter = 0
            # dy += square

        window.fill((100, 100, 100))
        make_shape(window, dx, dy, current_shape)
        make_grid(window, width, height, rows, cols)
        counter += 1
        dx, dy = 0, 0
        pg.display.update()


if __name__ == '__main__':
    main()
    pg.quit()
