import random
import sys

import pygame as pg

from shape import Shape

'''
Made by Tomasz Potoczko. 
This project is a simple incarnation of 
Tetris made using Pygame.
'''


# global variables
score = 0
prev_tetris = False


def update_grid_array(grid_array, tetrino):
    # this method will 'stain' the grid with all the tetrinos which have reached the bottom
    tetrino_grid_coords = tetrino.grid_coords[tetrino.rotation % len(tetrino.grid_coords)]
    for coordinates in tetrino_grid_coords:
        x, y = coordinates[0], coordinates[1]
        grid_array[y][x] = tetrino.colour

    return grid_array


def get_rand_shape():
    rand_shape = random.choice(["I", "J", "L", "O", "S", "T", "Z"])
    return Shape(rand_shape)


def update_screen_with_old_shapes(window, grid_array):
    # goes through the grid_array and checks if a position is not of the background colour
    # if it isn't it draws a rect there of the color that is there instead
    for row_idx, row in enumerate(grid_array):
        for col_idx, colour in enumerate(row):
            if colour != (100, 100, 100):
                pg.draw.rect(window, colour, (col_idx * 30, row_idx * 30, 30, 30))


def make_grid(window, width, height, rows, cols):
    # draws a grid on the screen
    distance_btw_rows = width // rows
    distance_btw_cols = height // cols
    x, y = 0, 0
    # draws vertical lines
    for i in range(rows):
        x += distance_btw_rows
        pg.draw.line(window, (0, 0, 0), (x, 0), (x, height))

    # draws horizontal lines
    for i in range(cols):
        y += distance_btw_cols
        pg.draw.line(window, (0, 0, 0), (0, y), (width, y))


def make_shape(window, dx, dy, tetrino):
    tetrino.make_shape(dx, dy)
    pg.draw.polygon(window, tetrino.colour, tetrino.shape)


def moveable_directions(tetrino, grid_array):
    # checks if the spaces to the right, left and below are available (coloured gray)
    directions = [1, 1, 1]  # left, right, down
    tetrino_grid_coords = tetrino.grid_coords[tetrino.rotation % len(tetrino.grid_coords)]

    # check if left squares are empty
    try:
        for coord in tetrino_grid_coords:
            if grid_array[coord[1]][coord[0] - 1] != (100, 100, 100):
                directions[0] = 0
                break
    except IndexError:
        directions[0] = 0

    # check if right squares are empty
    try:
        for coord in tetrino_grid_coords:
            if grid_array[coord[1]][coord[0] + 1] != (100, 100, 100):
                directions[1] = 0
                break
    except IndexError:
        directions[1] = 0
    # check if down squares are empty
    try:
        for coord in tetrino_grid_coords:
            if grid_array[coord[1] + 1][coord[0]] != (100, 100, 100):
                directions[2] = 0
                break
    except IndexError:
        # we pass because we want the code to run for one more square down
        # as to allow the player to move left and right just before the shape
        # is set
        pass

    return directions


def remove_full_bar(grid_array):
    # when a row is full it will delete that row
    global score, prev_tetris
    rows_deleted = 0
    add_score = 0
    for idx, row in enumerate(grid_array):
        remove_row = True

        for colour in row:
            if colour == (100, 100, 100):
                remove_row = False
                break

        if remove_row:
            # the row above becomes the considered row
            # until we get to the top and then top is set ro gray
            for i in range(idx, 1, -1):
                grid_array[i] = grid_array[i - 1]
            grid_array[0] = [(100, 100, 100) for _ in range(10)]

            add_score += 100
            rows_deleted += 1
            if rows_deleted == 4:
                if not prev_tetris:
                    add_score = 800
                else:
                    add_score = 1200

                prev_tetris = True

            else:
                prev_tetris = False

    # print(prev_tetris)
    # print(f'add_score {add_score}')
    score += add_score


def display_next_shape(window, tetrino):
    if not tetrino.shape:
        tetrino.make_shape(260, 450)
    pg.draw.polygon(window, tetrino.colour, tetrino.shape)


def main():
    global score
    # setting the window
    pg.init()
    size = width, height = 300, 600
    rows, cols = 10, 20
    window = pg.display.set_mode((500, 600))
    pg.display.set_caption("TETRIS")
    img = pg.image.load("data/logo.png").convert()
    pg.display.set_icon(img)

    # setting the fps
    clock = pg.time.Clock()
    clock.tick(60)

    # game initialisation
    grid_array = [[(100, 100, 100) for _ in range(10)] for _ in range(20)]
    square = 30  # used to denote the distance
    counter = 0  # used for counting frames
    current_shape = get_rand_shape()
    next_shape = get_rand_shape()
    moves = [1, 1, 1]
    font = pg.font.SysFont('Comic Sans MS', 25)
    next_shape_text = font.render('NEXT SHAPE: ', False, (0, 0, 0))
    restart_text = font.render('PRESS ANY BUTTON TO RESTART', False, (0, 0, 0))

    # game loop
    while 1:
        # break
        dx, dy = 0, 0
        score_text = font.render(f'Score: {score}', False, (0, 0, 0))
        level_text = font.render(f'Level: {score // 500 + 1}', False, (0, 0, 0))

        # get user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    dx += square
                if event.key == pg.K_LEFT:
                    dx -= square
                if event.key == pg.K_DOWN:
                    dy += square
                    score += 1
                if event.key == pg.K_UP:
                    # ROTATE
                    current_shape.rotate(grid_array)

        # every second or so the shape will drop by one square
        # they start to fall faster the further we are in the game
        if counter > 1000 - (score // 500 + 1) * 100:
            counter = 0
            dy += square

        # collision with colour blocks
        if counter > 0:
            moves = moveable_directions(current_shape, grid_array)

        # making sure we don't step over the window
        if current_shape.left < square or not moves[0]:
            if dx < 0:
                dx = 0

        if current_shape.right > width - square or not moves[1]:
            if dx > 0:
                dx = 0

        if not moves[2] and current_shape.top < 120:
            next_shape.x, next_shape.y = 4 * square, 30
            make_shape(window, 0, 0, next_shape)
            break

        # when we hit the bottom
        if current_shape.down > height or not moves[2]:
            # get new shape object and set it to the controlled one
            grid_array = update_grid_array(grid_array, current_shape)
            remove_full_bar(grid_array)
            next_shape.x, next_shape.y = 4 * square, 0
            next_shape.shape = []
            current_shape = next_shape
            next_shape = get_rand_shape()
            current_shape.x, current_shape.y = 4 * square, 0
            counter = 0

        window.fill((100, 100, 100))
        update_screen_with_old_shapes(window, grid_array)
        make_shape(window, dx, dy, current_shape)
        display_next_shape(window, next_shape)
        make_grid(window, width, height, rows, cols)
        counter += 1
        dx, dy = 0, 0
        window.blit(next_shape_text, (330, 400))
        window.blit(score_text, (330, 0))
        window.blit(level_text, (330, 200))
        pg.display.update()

    font = pg.font.SysFont('Comic Sans MS', 80)
    game_over_text = font.render('GAME OVER', False, (0, 0, 0))

    while 2:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                main()
        window.blit(game_over_text, (25, 200))
        window.blit(restart_text, (50, 300))

        pg.display.update()


if __name__ == '__main__':
    main()
    pg.quit()
