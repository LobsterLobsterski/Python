from MinHeap import MinHeap
from Robot import Robot
from functions import pg, update_screen
import sys


if __name__ == "__main__":
    width, height = 1000, 1000
    window = pg.display.set_mode((width, height))
    rows, cols = 50, 50
    square = width//cols, height//rows
    pg.display.set_caption("D* visualisation")

    grid_array = [[0 for _ in range(cols)] for _ in range(rows)]
    x_pos, y_pos = 0, 0
    robot = Robot(x_pos, y_pos, square, rows, cols)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
                if event.key == pg.K_RIGHT:
                    # x_pos += square[0]
                    robot.move(square[0], 0)
                if event.key == pg.K_LEFT:
                    # x_pos -= square[0]
                    robot.move(-square[0], 0)
                if event.key == pg.K_DOWN:
                    # y_pos += square[1]
                    robot.move(0, square[1])
                if event.key == pg.K_UP:
                    # y_pos -= square[1]
                    robot.move(0, square[1])

        update_screen(window, width, height, square, rows, cols, robot)

