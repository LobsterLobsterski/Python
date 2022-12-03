import pygame as pg


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


def is_valid(new_pos, rows, cols, square):
    # checks if the position proposed is one that is within boundaries and is not and obstacle
    if new_pos[0] > cols*square[0] or new_pos[0] < 0 or new_pos[1] > rows*square[1] or new_pos[1] < 0:
        return False

    return True


def draw_robot(robot, window, square, rows, cols):
    pg.draw.rect(window, (255, 0, 0), (robot.x_pos, robot.y_pos, square[0], square[1]))
    # for direction in [(0, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
    #     neighbour = robot.x_pos+square[0]*direction[0], robot.y_pos+square[1]*direction[1]
    #     if is_valid(neighbour, rows, cols, square):
    for neighbour in robot.visible_squares:
        pg.draw.rect(window, (150, 150, 150), (neighbour[0], neighbour[1], square[0], square[1]))


def update_screen(window, width, height, square, rows, cols, robot):
    window.fill((80, 80, 80))
    draw_robot(robot, window, square, rows, cols)
    make_grid(window, width, height, rows, cols)
    pg.display.update()


