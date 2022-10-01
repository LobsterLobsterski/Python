import sys

from PathFinding import PF
from functions import *


def main():
    # setting the window
    pg.init()
    size = width, height = 500, 500
    dim = rows, cols = 25, 25
    square = width//cols, height//rows
    window = pg.display.set_mode(size)
    pg.display.set_caption("A* Algorythm")

    # init
    grid_array = [[0 for _ in range(cols)] for _ in range(rows)]
    path = []
    visualiser_list = []
    visualiser_list_on = False
    counter = 0

    # main loop
    while True:
        pressed = False
        square_clicked = -1, -1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
                if event.key == pg.K_RETURN:
                    path = []
                    pressed = True
                    init = time.time()
                    pf = PF(grid_array)

                    try:
                        path, path_cost, visualiser_list = pf.find_path(True)
                    except (ValueError, TypeError):
                        return
                    print(f'full execution time is: {time.time()-init}')
                    print(f'{path=}')
                    print(f'{path_cost=}')
                    if visualiser_list:
                        visualiser_list_on = True

                if event.key == pg.K_r:
                    grid_array = [[0 for _ in range(cols)] for _ in range(rows)]
                    path = []
                    visualiser_list = []
                    counter = 0
                    visualiser_list_on = False

                if event.key == pg.K_SPACE:
                    path = []
                    pressed = True

                if event.key == pg.K_o:
                    pass

            if event.type == pg.MOUSEBUTTONDOWN:
                square_clicked = round_to_nearest_square(pg.mouse.get_pos(), square)

                # when left mouse button is clicked we add a square
                if pg.mouse.get_pressed()[0]:
                    grid_array = set_square_state(grid_array, square_clicked, 0)
                # when the right is pressed we remove a square
                elif pg.mouse.get_pressed()[2]:
                    grid_array = set_square_state(grid_array, square_clicked, 1)

        window.fill((100, 100, 100))
        grid_array = add_path(grid_array, path, pressed)
        draw_start_end_obstacles(window, grid_array, square)
        if visualiser_list_on:
            draw_visaliser(window, square, visualiser_list, counter)
            counter += 1
            if counter > len(visualiser_list):
                counter = len(visualiser_list)
        if counter == len(visualiser_list):
            draw_path(window, grid_array, square)

        make_grid(window, size, dim, square)
        pg.display.update()


if __name__ == '__main__':
    main()
    pg.quit()
