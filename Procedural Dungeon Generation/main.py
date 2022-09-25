import sys
import time
import tkinter as tk

from functions import *
from menu import Menu

'''
Main file where all the magic happens.
Procedural Dungeon Map Generator created by Tomasz Potoczko.
Titled as D&D Map Generator as it's what I use it for but can 
be used for any game (hopefully).
'''


def main(width, height, max_rooms, small_rooms=0, big_rooms=0, caveify_val=1000):
    # setting the window
    pg.init()
    size = width, height
    size_mod = 4
    square = 30//size_mod, 30//size_mod
    dim = rows, cols = height//square[0]+1, width//square[1]+1
    window = pg.display.set_mode(size)
    pg.display.set_caption("D&D dungeon generator")
    print(f'{cols}x{rows}')

    # main loop initialisation
    grid_array = [[3 for _ in range(cols)] for _ in range(rows)]
    rooms = []
    click_counter = 0
    start = 0
    end = 0

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

                if event.key == pg.K_SPACE:
                    # reset to create a new map
                    rooms = []
                    grid_array = [[3 for _ in range(cols)] for _ in range(rows)]

                    if small_rooms and big_rooms:
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
                        rooms = make_rooms(cols, rows, big_rooms, (big_room_w_min, big_room_w_max),
                                           (big_room_h_min, big_room_h_max), rooms, size_mod)
                        # make small rooms
                        rooms = make_rooms(cols, rows, small_rooms, (small_room_w_min, small_room_w_max),
                                           (small_room_h_min, small_room_h_max), rooms, size_mod)
                    else:
                        rooms = make_rooms(cols, rows, max_rooms, (6, 15), (6, 15), rooms, size_mod)

                    grid_array = draw_rooms(grid_array, rooms)
                    # make corridors
                    grid_array = draw_corridors(grid_array, rooms, size_mod)

                if event.key == pg.K_c:
                    grid_array = caveify(grid_array, cols, rows, caveify_val)

            if event.type == pg.MOUSEBUTTONDOWN:
                # allows the user to add some hand-made corrections

                square_clicked = round_to_nearest_square(pg.mouse.get_pos(), square)
                # print(f'{square_clicked=}')

                # when left mouse button is clicked we add a square
                if pg.mouse.get_pressed()[0]:
                    if click_counter % 2 == 0:
                        start = square_clicked
                        click_counter += 1
                    else:
                        end = square_clicked
                        click_counter += 1

                    if start and end:
                        if end[0] < start[0] or end[1] < start[1]:
                            temp = end
                            end = start
                            start = temp
                        if end[0] > start[0] and end[1] < start[1]:
                            temp_s = start[0], end[1]
                            temp_e = end[0], start[1]
                            start = temp_s
                            end = temp_e

                        rooms.append(Rect(start[1], start[0], end[0]-start[0]+1, end[1]-start[1]+1))
                        start = None
                        end = None

                if pg.mouse.get_pressed()[2]:
                    # instead allow the player to delete a square (just change colour)
                    pass
                    # rooms.append(Rect(square_clicked[1], square_clicked[0], 2, 2))

        window.fill((100, 100, 100))
        grid_array = draw_rooms(grid_array, rooms)
        place_squares(window, grid_array, square)
        make_grid(window, size, dim, square, size_mod)
        pg.display.update()


def menu():
    # first screen user sees which allows them input the dungeon params

    root = tk.Tk(className=" D&D dungeon generator")
    root.geometry('500x800')
    root.minsize(500, 800)
    root.maxsize(500, 800)
    root.configure(bg='#646464')

    men = Menu(root)

    root.mainloop()

    # print(f'{men.width, men.height, men.max_rooms, men.small_rooms, men.big_rooms, men.caveify_val =}')
    main(men.width, men.height, men.max_rooms, men.small_rooms, men.big_rooms, men.caveify_val)


if __name__ == '__main__':
    menu()
    # main(1280, 720, 10, 8, 4)
    # main(300, 300, 4)
    pg.quit()

