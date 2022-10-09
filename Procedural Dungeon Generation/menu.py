import tkinter as tk

"""
Not gonna sugar coat it, i hate tkinter. 
Simple menu class allowing a GUI for the user inputs
as well as for handling all of the labels,
entry boxes e.t.c.
"""


class Menu:
    def __init__(self, root):
        self._root = root
        self._width, self._height = 0, 0
        self._max_rooms = 0
        self._caveify_val = 0
        self._submitted = False
        self._small_rooms = 0
        self._big_rooms = 0
        self._circular_rooms = 0

        self._grid_off = False

        self._advanced_room_settings = False
        self._advanced_map_settings = False
        self._caveify_on = False
        self._rect_on = True
        self._circ_on = False
        self._resolution = tk.IntVar()
        self._resolution.set(1)
        self._colour = tk.IntVar()
        self._colour.set(0)

        self._advanced_map_size = [0 for _ in range(5)]
        self._labels = [0 for _ in range(6)]
        self._entries = [0 for _ in range(6)]
        self._caveify = [0 for _ in range(3)]
        self._other = [0 for _ in range(2)]
        self._advanced_settings = [0 for _ in range(13)]
        self._advanced_check_box = ...

        self._var_width = tk.StringVar()
        self._var_height = tk.StringVar()
        self._var_max_rooms = tk.StringVar()
        self._var_small_rooms = tk.StringVar()
        self._var_big_rooms = tk.StringVar()
        self._var_caveify_val = tk.StringVar()
        self._var_circular_rooms = tk.StringVar()
        self._var_circular_rooms.set("0")

        self.init_objects()

    def submitted(self):
        return self._submitted

    @staticmethod
    def get_shade(shade):
        # default gray tile
        if shade == 0:
            return 130, 130, 130

        # for brown maps
        elif shade == 1:
            return 92, 64, 51

        # for green maps
        elif shade == 2:
            return 14, 90, 14

        # for off-white maps
        elif shade == 3:
            return 169, 169, 169

        # for dark-gray maps
        elif shade == 4:
            return 110, 110, 110

        # for brownish-red maps
        elif shade == 5:
            return 109, 42, 20

        # for sandy maps
        elif shade == 6:
            return 224, 144, 76

    def return_vals(self):
        print(self._colour.get())
        return self._width, self._height, self._max_rooms, self.get_shade(self._colour.get()), self._small_rooms, self._big_rooms, self._circular_rooms, \
               self._caveify_val, self._grid_off, self._circ_on

    def submit_click(self):
        # saves the inputted values and exits the tkinter loop
        if not self._advanced_map_settings:
            if self._resolution.get() > 0:
                if self._resolution.get() == 1:
                    self._var_width.set("1920")
                    self._var_height.set("1080")
                elif self._resolution.get() == 2:
                    self._var_width.set("2048")
                    self._var_height.set("1080")
                elif self._resolution.get() == 3:
                    self._var_width.set("3840")
                    self._var_height.set("2160")

        self._width, self._height = int(self._var_width.get()), int(self._var_height.get())
        try:
            self._small_rooms = int(self._var_small_rooms.get())
            self._big_rooms = int(self._var_big_rooms.get())
        except ValueError:
            self._small_rooms = 0
            self._big_rooms = 0
            try:
                self._max_rooms = int(self._var_max_rooms.get())
            except ValueError:
                self._max_rooms = 0
        try:
            if self._caveify_on:
                self._caveify_val = int(self._var_caveify_val.get())
            self._circular_rooms = int(self._var_circular_rooms.get())
        except ValueError:
            return

        self._submitted = True
        self._root.destroy()

    def change(self, val):
        # it's for changing check box states
        if val == 0:
            self._advanced_room_settings = not self._advanced_room_settings
        elif val == 1:
            self._advanced_map_settings = not self._advanced_map_settings

        elif val == 2:
            self._caveify_on = not self._caveify_on

        elif val == 3:
            self._grid_off = not self._grid_off

        elif val == 4:
            self._rect_on = not self._rect_on

        elif val == 5:
            self._circ_on = not self._circ_on

        self.place_objects()

    def init_objects(self):
        # initialises all the _labels and so on

        # here we initialise the map size stuff
        self._labels[0] = tk.Label(self._root, text="Map width:", font=30)
        self._advanced_map_size[0] = tk.Label(self._root, text="Map size:", font=30)
        self._advanced_map_size[1] = tk.Radiobutton(self._root, text="HD", font=30, value=1, variable=self._resolution)

        self._advanced_map_size[2] = tk.Radiobutton(self._root, text="2k", font=30, value=2, variable=self._resolution)
        self._advanced_map_size[3] = tk.Radiobutton(self._root, text="4k", font=30, value=3, variable=self._resolution)
        self._advanced_map_size[4] = tk.Checkbutton(self._root, text="Custom", font=30, command=lambda: self.change(1))
        self._labels[1] = tk.Label(self._root, text="Map height:", font=30)

        # here we initialise the amount of rooms stuff
        self._labels[2] = tk.Label(self._root, text="Max rand rooms:", font=30)
        self._labels[3] = tk.Label(self._root, text="Advanced:", font=30)
        self._advanced_check_box = tk.Checkbutton(self._root, command=lambda: self.change(0))
        self._advanced_settings[0] = tk.Label(self._root, text="Room shapes:", font=30)
        self._advanced_settings[1] = tk.Checkbutton(self._root, text="rectangular", font=30, command=lambda: self.change(4))

        self._advanced_settings[2] = tk.Checkbutton(self._root, text="circular", font=30, command=lambda: self.change(5))
        self._advanced_settings[3] = tk.Label(self._root, text="number of circular rooms:", font=30)
        self._advanced_settings[4] = tk.Entry(self._root, textvariable=self._var_circular_rooms, font=30)

        self._advanced_settings[5] = tk.Label(self._root, text="Colour scheme:", font=30)
        self._advanced_settings[6] = tk.Radiobutton(self._root, text="Gray Tile", font=30, value=0, variable=self._colour)

        self._advanced_settings[7] = tk.Radiobutton(self._root, text="Dirt road", font=30, value=1, variable=self._colour)
        self._advanced_settings[8] = tk.Radiobutton(self._root, text="Forest", font=30, value=2, variable=self._colour)
        self._advanced_settings[9] = tk.Radiobutton(self._root, text="Off-white", font=30, value=3, variable=self._colour)
        self._advanced_settings[10] = tk.Radiobutton(self._root, text="Cavern", font=30, value=4, variable=self._colour)
        self._advanced_settings[11] = tk.Radiobutton(self._root, text="Red Earth", font=30, value=5, variable=self._colour)
        self._advanced_settings[12] = tk.Radiobutton(self._root, text="Dunes", font=30, value=6, variable=self._colour)

        self._labels[4] = tk.Label(self._root, text="Big rooms: ", font=30)
        self._labels[5] = tk.Label(self._root, text="Small rooms: ", font=30)

        self._caveify[0] = tk.Checkbutton(self._root, text="Caveify on:", font=30, command=lambda: self.change(2))
        self._caveify[1] = tk.Label(self._root, text="Degree of Caveification:", font=30)
        self._caveify[2] = tk.Label(self._root, text="*much higher values are recommended for higher resolutions", font=("Comic Sans", "10", "italic"))

        # and here we intialise the entry boxes
        self._entries[0] = tk.Entry(self._root, textvariable=self._var_width, font=30)
        self._entries[1] = tk.Entry(self._root, textvariable=self._var_height, font=30)
        self._entries[2] = tk.Entry(self._root, textvariable=self._var_max_rooms, font=30)
        self._entries[3] = tk.Entry(self._root, textvariable=self._var_small_rooms, font=30)
        self._entries[4] = tk.Entry(self._root, textvariable=self._var_big_rooms, font=30)
        self._entries[5] = tk.Entry(self._root, textvariable=self._var_caveify_val, font=30)

        # other stuff
        self._other[0] = tk.Checkbutton(self._root, text="Grid OFF", font=30, command=lambda: self.change(3))
        self._other[1] = tk.Button(self._root, text="Submit", font=30, command=lambda: self.submit_click())

        self.place_objects()

    def place_objects(self):
        # takes all the initialised 'objects' and places them on the screens

        x, y = 40, 50
        for idx in range(len(self._advanced_map_size)):
            if idx == 0:
                self._advanced_map_size[idx].place(x=20, y=50)
            else:
                self._advanced_map_size[idx].place(x=x, y=y)
            x += 80

        y = 100
        x = 20
        for idx in range(len(self._labels)):
            if idx == 3:
                y2 = y
            self._labels[idx].place(x=x, y=y)
            y += 50

        self._advanced_check_box.place(x=120, y=y2)

        x = 20
        for obj in self._caveify:
            obj.place(x=x, y=y)
            y += 50

        x = 200
        y = 100
        for idx in range(len(self._entries)):
            if idx == 3:
                y += 50
            elif idx == 5:
                y += 50
                x += 50
                self._var_caveify_val.set('1000')

            self._entries[idx].place(x=x, y=y)
            y += 50

        x = 20
        y += 50
        for obj in self._other:
            obj.place(x=x, y=y)

        x = 500
        y = 50
        for obj in self._advanced_settings:
            obj.place(x=x, y=y)
            y += 50

        self._other[1].place(x=150, y=700)

        # if some check boxes are checked we have to 'forget' to place some things
        if not self._advanced_map_settings:
            self._labels[0].place_forget()
            self._labels[1].place_forget()
            self._entries[0].place_forget()
            self._entries[1].place_forget()
        else:
            for idx in range(len(self._advanced_map_size) - 1):
                self._advanced_map_size[idx].place_forget()

        if not self._advanced_room_settings:
            self._labels[4].place_forget()
            self._labels[5].place_forget()
            self._entries[3].place_forget()
            self._entries[4].place_forget()
            self._advanced_settings[0].place_forget()
            self._advanced_settings[1].place_forget()
            self._advanced_settings[2].place_forget()
            self._advanced_settings[3].place_forget()
            self._advanced_settings[5].place_forget()
            self._advanced_settings[6].place_forget()
            self._advanced_settings[7].place_forget()
            self._advanced_settings[8].place_forget()
            self._advanced_settings[9].place_forget()
            self._advanced_settings[10].place_forget()
            self._advanced_settings[11].place_forget()
            self._advanced_settings[12].place_forget()


        else:
            self._labels[2].place_forget()
            self._entries[2].place_forget()


        if not self._circ_on:
            self._advanced_settings[3].place_forget()
            self._advanced_settings[4].place_forget()

        if not self._caveify_on:
            self._caveify[1].place_forget()
            self._caveify[2].place_forget()
            self._entries[5].place_forget()

        self._advanced_map_size[1].select()
        self._advanced_settings[1].select()
        self._advanced_settings[6].select()


