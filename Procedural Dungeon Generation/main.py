import sys

from functions import *
from menu import Menu
import tkinter as tk

'''
Procedural Dungeon Map Generator v0.9 created by Tomasz Potoczko.
Titled as D&D Map Generator as it's what I use it for but can 
be used for any game.
Creates a number of rooms based on the user input then creates corridors between these rooms.
Also allows the user to number the rooms, caveify them and choose a shader for the tiles.
'''


def main(width, height, max_rooms, shade, small_rooms=0, big_rooms=0, circular_rooms=0, caveify_val=0, grid_off=False, circles_on=False):
    # setting the window
    pg.init()
    SIZE = width, height
    SIZE_MOD = 4
    SQUARE = 30 // SIZE_MOD, 30 // SIZE_MOD
    DIM = ROWS, COLS = height // SQUARE[0] + 1, width // SQUARE[1] + 1
    window = pg.display.set_mode(SIZE)
    pg.display.set_caption("D&D Dungeon Generator")
    # print(f'{COLS}x{ROWS}')

    # main loop initialisation
    grid_array = [[3 for _ in range(COLS)] for _ in range(ROWS)]
    numbers_on = False
    rooms = []
    start_screen = True

    # main loop
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
                if event.key == pg.K_RETURN:
                    save_map(window)
                if event.key == pg.K_BACKSPACE:
                    pg.quit()
                    return True

                if event.key == pg.K_SPACE:
                    start_screen = False
                    # reset to create a new map
                    rooms = []
                    grid_array = [[3 for _ in range(COLS)] for _ in range(ROWS)]

                    if small_rooms or big_rooms:
                        # arbitrary (for now) values
                        big_room_w_min = 7
                        big_room_w_max = 12
                        big_room_h_min = 7
                        big_room_h_max = 12

                        small_room_w_min = 4
                        small_room_w_max = 7
                        small_room_h_min = 4
                        small_room_h_max = 7

                        # make big rooms
                        rooms = make_rooms(rooms, COLS, ROWS, big_rooms, SIZE_MOD,
                                           room_width_range=(big_room_w_min, big_room_w_max),
                                           room_height_range=(big_room_h_min, big_room_h_max))

                        rooms = make_rooms(rooms, COLS, ROWS, small_rooms, SIZE_MOD,
                                           room_width_range=(small_room_w_min, small_room_w_max),
                                           room_height_range=(small_room_h_min, small_room_h_max))

                        if circles_on:
                            rooms = make_rooms(rooms, COLS, ROWS, circular_rooms, SIZE_MOD, radius_range=(3, 5))

                        # print(f'{rooms=}')

                    else:
                        big_room_w_min = 6
                        big_room_w_max = 12
                        big_room_h_min = 6
                        big_room_h_max = 12

                        small_room_w_min = 3
                        small_room_w_max = 7
                        small_room_h_min = 3
                        small_room_h_max = 7

                        num_of_rooms = max_rooms//3 if circles_on else max_rooms//2

                        rooms = make_rooms(rooms, COLS, ROWS, num_of_rooms, SIZE_MOD,
                                           room_width_range=(big_room_w_min, big_room_w_max),
                                           room_height_range=(big_room_h_min, big_room_h_max))

                        rooms = make_rooms(rooms, COLS, ROWS, num_of_rooms, SIZE_MOD,
                                           room_width_range=(small_room_w_min, small_room_w_max),
                                           room_height_range=(small_room_h_min, small_room_h_max))
                        if circles_on:
                            rooms = make_rooms(rooms, COLS, ROWS, max_rooms//3, SIZE_MOD, radius_range=(3, 5))

                    grid_array = draw_rooms(grid_array, rooms)

                    # make corridors
                    grid_array = draw_corridors(grid_array, rooms, SIZE_MOD)

                if event.key == pg.K_c:
                    grid_array = caveify(grid_array, COLS, ROWS, caveify_val)

                if event.key == pg.K_n:
                    numbers_on = not numbers_on

                # debug key
                if event.key == pg.K_d:
                    pass

            update_screen(window, grid_array, rooms, numbers_on, grid_off, SQUARE, SIZE, DIM, SIZE_MOD, shade, start_screen)


def menu():
    # first screen user sees which allows them input the dungeon params
    returned = True
    while returned:
        root = tk.Tk(className=" D&D dungeon generator")
        root.geometry('800x800')
        root.minsize(800, 800)
        root.maxsize(800, 800)
        root.configure(bg='#646464')

        men = Menu(root)

        root.mainloop()

        # print(f'{men._width, men._height, men._max_rooms, men._small_rooms, men._big_rooms, men._caveify_val =}')
        if men.submitted():
            width, height, max_rooms, shade, small_rooms, big_rooms, circular_rooms, caveify_val, grid_off, circles_on = men.return_vals()
            returned = main(width, height, max_rooms, shade, small_rooms, big_rooms, circular_rooms, caveify_val, grid_off, circles_on)
        else:
            sys.exit()


if __name__ == '__main__':
    menu()
    # main(1280, 720, 6, 0, 0, 0, 1000, 0, 0)
    pg.quit()

