import os
import random
import time

import pygame as pg
from Room import *
from os import listdir


'''
File containing all the loose methods required by the program.
'''


def round_to_nearest_square(pixel_coords, square, size_mod):
    # 'translates' pixel coordinates from a mouse-click to a grid position
    square = square[0]*size_mod, square[1]*size_mod
    return pixel_coords[0] // square[0], pixel_coords[1] // square[1]


def update_screen(window, grid_array, rooms, numbers_on, grid_off, square, size, dim, size_mod, shade, start_screen):
    # groups all the code related to setting stuff on the screen

    window.fill((100, 100, 100))
    if start_screen:
        myfont = pg.font.SysFont("ariel", 35, bold=True)
        text = ["Controls: ", "Space:  Generates the dungeon", "Enter:  Saves the map", "Escape:  exits the program",
                "Backspace:  Returns to the menu", "c:  caveifies the dungeon", "c:  numbers the rooms"]
        labels = []
        for t in text:
            label = myfont.render(t, True, (30, 30, 30))
            labels.append(label)

        y = 100
        for label in labels:
            window.blit(label, (size[0]//3, y))
            y += 100
    else:
        colour_the_grid(window, grid_array, square, shade)
        make_grid(window, size, dim, square, size_mod, grid_off)
        add_room_labels(window, rooms, square, numbers_on)
    pg.display.update()


def caveify(grid_array, cols, rows, amount):
    # makes the map less regular and more 'natural' by randomly adding smaller tiles
    tiles_placed = 0
    while tiles_placed < amount:
        rand_y = random.randint(0, cols-1)
        rand_x = random.randint(0, rows-2)

        if grid_array[rand_x][rand_y] in [5, 6, 7, 8]:

            neighbours = [(rand_x-1, rand_y), (rand_x, rand_y+1), (rand_x+1, rand_y), (rand_x, rand_y-1)]
            for x, y in neighbours:
                try:
                    val = grid_array[x][y]
                except IndexError:
                    continue

                if grid_array[x][y] == 3:
                    grid_array[x][y] = get_random_shade()
                    tiles_placed += 1
                    break

    return grid_array


def save_map(window):
    # responsible for saving the created map permanently
    try:
        try:
            last = sorted(listdir("Saved Maps"), key=len)[len(listdir("Saved Maps"))-1]
            val = ""
            for char in last:
                if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    val = val+char

            val = int(val) + 1
        except IndexError:
            val = 1
        pg.image.save(window, f"Saved Maps/map{val}.jpg")
    except FileNotFoundError:
        os.mkdir("Saved Maps")
        save_map(window)


def add_room_labels(window, rooms, square, numbers_on):
    # labels the rooms from 1 to n, where n is the number of rooms
    if numbers_on:
        font = pg.font.SysFont('ariel', 32)
        for idx, room in enumerate(rooms):
            text = font.render(str(idx+1), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = room.centre(square)
            window.blit(text, textRect)


def make_grid(window, size, dim, square, size_mod, grid_off):
    # draws a grid on the screen
    if not grid_off:
        square = square[0]*size_mod, square[1]*size_mod
        x, y = 0, 0
        for i in range(dim[1]):
            x += square[0]
            pg.draw.line(window, (0, 0, 0), (x, 0), (x, size[1]))

        for i in range(dim[0]):
            y += square[1]
            pg.draw.line(window, (0, 0, 0), (0, y), (size[0], y))


def make_rooms(rooms, cols, rows, max_rooms, size_mod, **kwargs):
    # creates rooms of random size as dictated by the params

    # these should be passed by Rect rooms
    room_width_range = kwargs.get('room_width_range')
    room_height_range = kwargs.get('room_height_range')

    # these should be passed by Circle rooms
    radius_range = kwargs.get('radius_range')

    num_of_rooms_created = 0
    while num_of_rooms_created < max_rooms:
        rand_x, rand_y = random.randint(0, cols), random.randint(0, rows)
        if radius_range:
            rand_r = random.randint(radius_range[0], radius_range[1])
            room = Circle((rand_x, rand_y), rand_r, size_mod)

        elif room_width_range:
            rand_w = random.randint(room_width_range[0], room_width_range[1])
            rand_h = random.randint(room_height_range[0], room_height_range[1])
            room = Rect(rand_x, rand_y, rand_w, rand_h, size_mod)

        if valid_room_placement((rows, cols), room):
            continue

        if room_collision(room, rooms, size_mod):
            continue

        rooms.append(room)
        num_of_rooms_created += 1

    return rooms


def valid_room_placement(dim, room):
    # checks if the passed in room would be outside of bounds
    if room.left < 1 or room.right > dim[0]-1 or room.top < 1 or room.down > dim[1]-1:
        return True
    return False


def room_collision(new_room, rooms, size_mod):
    # checks if the passed in room is colliding with another one
    # it's not perfect, but it does the job

    for existing_room in rooms:
        if new_room.left < existing_room.right+size_mod and new_room.right > existing_room.left+size_mod \
                and new_room.top < existing_room.down+size_mod and new_room.down > existing_room.top+size_mod:
            return True

    return False


def draw_corridors(grid_array, rooms, size_mod):
    # draws corridors between rooms from and to random positions within these rooms
    # creating pathways to traverse the map

    # for more linear/coherent/sane map
    # rooms = sorted(rooms)

    size_mod_adjustment = [(x, y) for x in range(size_mod) for y in range(size_mod)]
    for idx in range(len(rooms)-1):
        room_start = rooms[idx]
        room_end = rooms[idx+1]

        while True:
            rand_start = random.randint(room_start.left, room_start.right-size_mod), random.randint(room_start.top, room_start.down-size_mod)
            rand_end = random.randint(room_end.left, room_end.right-size_mod), random.randint(room_end.top, room_end.down-size_mod)
            if rand_start[0] == rand_end[0] or rand_start[1] == rand_end[1]:
                continue
            if rand_start in room_start.points and rand_end in room_end.points:
                break

        # width is cols (x)
        # height is rows (y)

        width = rand_end[0]-rand_start[0]
        height = rand_end[1]-rand_start[1]

        d2 = random.randint(0, 1)

        if d2 % 2 == 0:
            step = 1 if width > 0 else -1
            for w in range(rand_start[0], rand_start[0]+width, step):
                for x_mod, y_mod in size_mod_adjustment:

                    grid_array[w+x_mod][rand_start[1]+y_mod+height] = get_random_shade()
            step = 1 if height > 0 else -1
            for h in range(rand_start[1], rand_start[1]+height, step):
                for x_mod, y_mod in size_mod_adjustment:
                    grid_array[rand_start[0]+x_mod][h+y_mod] = get_random_shade()
        else:
            step = 1 if width > 0 else -1
            for w in range(rand_start[0], rand_start[0]+width, step):
                for x_mod, y_mod in size_mod_adjustment:
                    grid_array[w+x_mod][rand_start[1]+y_mod] = get_random_shade()
            step = 1 if height > 0 else -1
            for h in range(rand_start[1], rand_start[1]+height, step):
                for x_mod, y_mod in size_mod_adjustment:
                    grid_array[rand_start[0]+x_mod+width][h+y_mod] = get_random_shade()

    return grid_array


def draw_rooms(grid_array, rooms):
    # takes the rooms and adds them to the grid array
    for room in rooms:
        for coord in room.points:
            grid_array[coord[0]][coord[1]] = get_random_shade()

    return grid_array


def get_random_shade():
    # returns a random integer value which will dictate its
    # colour in colour_the_grid method
    d300 = random.randint(0, 300)
    if d300 < 240:
        return 5
    elif 239 < d300 < 270:
        return 6
    elif 269 < d300 < 300:
        return 7
    else:
        return 8


def colour_the_grid(window, grid_array, square, shade):
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
            # walkable tiles
            elif val == 4:
                colour = 130, 130, 130

            if val == 5:
                # base
                colour = shade
            if val == 6:
                colour = (shade[0]-2 if shade[0] > 2 else 0, shade[1]-9 if shade[0] > 9 else 0,
                          shade[2]-11 if shade[2] > 11 else 0)
            if val == 7:
                colour = (shade[0]+11, shade[1]+6, shade[2]+10)
            if val == 8:
                # mix shade with 22, 22, 22
                colour = ((shade[0]+22)//2, (shade[1]+22)//2, (shade[2]+22)//2)

            if colour:
                coords = row_idx*square[1], col_idx*square[0]
                pg.draw.rect(window, colour, (coords[1], coords[0], square[0], square[1]))


