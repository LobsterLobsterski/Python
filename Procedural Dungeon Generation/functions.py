import random
import pygame as pg
from Room import Rect
from os import listdir

'''
File containing all the loose methods required by the program.
Moved here from main.py to make both more readable and cleaner.
'''


def caveify(grid_array, cols, rows, amount):
    # makes the map less regular and more 'natural' by adding some random tiles
    counter = 0
    while counter < amount:
        rand_y = random.randint(0, cols-1)
        rand_x = random.randint(0, rows-2)

        if grid_array[rand_x][rand_y] == 4:

            neighbours = [(rand_x-1, rand_y), (rand_x, rand_y+1), (rand_x+1, rand_y), (rand_x, rand_y-1)]
            for x, y in neighbours:
                try:
                    val = grid_array[x][y]
                except IndexError:
                    continue

                if grid_array[x][y] == 3:
                    grid_array[x][y] = 4
                    counter += 1
                    break

    return grid_array


def save_map(window):
    # responsible for saving the created map permanently
    try:
        last = sorted(listdir("saved_maps"), key=len)[len(listdir("saved_maps"))-1]
        val = ""
        for char in last:
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                val = val+char

        val = int(val) + 1
    except IndexError:
        val = 1
    pg.image.save(window, f"saved_maps/map{val}.jpg")


def make_grid(window, size, dim, square, size_mod):
    # draws a grid on the screen
    square = square[0]*size_mod, square[1]*size_mod
    x, y = 0, 0
    for i in range(dim[1]):
        x += square[0]
        pg.draw.line(window, (0, 0, 0), (x, 0), (x, size[1]))

    for i in range(dim[0]):
        y += square[1]
        pg.draw.line(window, (0, 0, 0), (0, y), (size[0], y))


def make_rooms(cols, rows, max_rooms, room_width_range, room_height_range, rooms, size_mod):
    # creates rooms of random size as dictated by the params

    num_of_rooms_created = 0
    while num_of_rooms_created < max_rooms:
        rand_x, rand_y = random.randint(0, cols), random.randint(0, rows)
        rand_w = random.randint(room_width_range[0], room_width_range[1])
        rand_h = random.randint(room_height_range[0], room_height_range[1])
        room = Rect(rand_x, rand_y, rand_w, rand_h, size_mod)
        if not valid_room_placement((rows, cols), room):
            continue
        if room_collision(room, rooms, size_mod):
            continue
        rooms.append(room)
        num_of_rooms_created += 1

    return rooms


def round_to_nearest_square(coords, square, size_mod):
    # 'translates' pixel coordinates from a mouse-click to
    # a grid position
    square = square[0]*size_mod, square[1]*size_mod
    return coords[0]//square[0], coords[1]//square[1]


def draw_rooms(grid_array, rooms):
    # takes the rooms and adds them to the grid array
    for room in rooms:
        for row_idx in range(room.y1, room.y2):
            for col_idx in range(room.x1, room.x2):
                grid_array[row_idx][col_idx] = 4

    return grid_array


def valid_room_placement(dim, room):
    # checks if the passed in room would be outside of bounds
    if room.x1 < 0 or room.x2 > dim[1]-1 or room.y1 < 0 or room.y2 > dim[0]-1:
        return False

    return True


def draw_corridors(grid_array, rooms, size_mod):
    # draws corridors between each room randomly
    # creating a non-linear pathways to traverse the map

    size_mod_adjustment = [(x, y) for x in range(size_mod) for y in range(size_mod)]
    for idx in range(len(rooms)-1):
        room_start = rooms[idx]
        room_end = rooms[idx+1]
        rand_start = (random.randint(room_start.x1, room_start.x2-size_mod), (random.randint(room_start.y1, room_start.y2-size_mod)))
        rand_end = (random.randint(room_end.x1, room_end.x2-size_mod), (random.randint(room_end.y1, room_end.y2-size_mod)))

        # _width is cols
        # _height is rows
        width = rand_end[0]-rand_start[0]
        height = rand_end[1]-rand_start[1]

        d2 = random.randint(0, 1)
        if d2 % 2 == 0:
            step = 1 if width > 0 else -1
            for w in range(rand_start[0], rand_start[0]+width, step):
                for x_mod, y_mod in size_mod_adjustment:
                    grid_array[rand_start[1]+height+x_mod][w+y_mod] = 4

            step = 1 if height > 0 else -1
            for h in range(rand_start[1], rand_start[1]+height, step):
                for x_mod, y_mod in size_mod_adjustment:
                    grid_array[h+x_mod][rand_start[0]+y_mod] = 4
        else:
            step = 1 if width > 0 else -1
            for w in range(rand_start[0], rand_start[0]+width, step):
                for x_mod, y_mod in size_mod_adjustment:
                    grid_array[rand_start[1]+x_mod][w+y_mod] = 4

            step = 1 if height > 0 else -1
            for h in range(rand_start[1], rand_start[1]+height, step):
                for x_mod, y_mod in size_mod_adjustment:
                    grid_array[h+x_mod][rand_start[0]+width+y_mod] = 4

    return grid_array


def room_collision(new_room, rooms, size_mod):
    # checks if the passed in room is colliding with another one
    for valid_room in rooms:
        if new_room.x1 < valid_room.x2+size_mod and new_room.x2 > valid_room.x1+size_mod \
                and new_room.y1 < valid_room.y2+size_mod and new_room.y2 > valid_room.y1+size_mod:
            return True

    return False


def place_squares(window, grid_array, square):
    # colours the grid in depending on the values in grid_array
    for row_idx, row in enumerate(grid_array):
        for col_idx, val in enumerate(row):
            colour = False
            # start
            if val == 1:
                colour = 0, 0, 255
            # end
            elif val == 2:
                colour = 0, 255, 0
            # wall
            elif val == 3:
                colour = 50, 50, 50
            # walkable tile
            elif val == 4:
                colour = 130, 130, 130
            # spare one for later
            elif val == 5:
                colour = 255, 0, 0

            if colour:
                coords = row_idx*square[1], col_idx*square[0]
                pg.draw.rect(window, colour, (coords[1], coords[0], square[0], square[1]))
