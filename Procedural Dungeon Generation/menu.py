import tkinter as tk

"""
Not gonna sugar coat it, i hate tkinter. 
Simple menu class allowing a GUI for the user inputs
as well as for handling all of the _labels,
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
        self._grid_off = False

        self._advanced_room_settings = False
        self._advanced_map_settings = False
        self._caveify_on = False
        self._val = tk.IntVar()
        # self._val.set(0)
        self._advanced_map_size = [0 for _ in range(5)]
        self._labels = [0 for _ in range(6)]
        self._entries = [0 for _ in range(6)]
        self._caveify = [0 for _ in range(3)]
        self._other = [0 for _ in range(1)]
        self._check_box = ...
        self._submit = tk.Button(self._root, text="Submit", font=30, command=lambda: self.submit_click())

        self._var1 = tk.StringVar()
        self._var2 = tk.StringVar()
        self._var3 = tk.StringVar()
        self._var4 = tk.StringVar()
        self._var5 = tk.StringVar()
        self._var6 = tk.StringVar()

        self.init_objects()

    def submitted(self):
        return self._submitted

    def return_vals(self):
        return self._width, self._height, self._max_rooms, self._small_rooms, self._big_rooms, self._caveify_val, self._grid_off

    def submit_click(self):
        # saves the inputted values and exits the tkinter loop
        self._submitted = True
        if self._val.get() == 1:
            self._var1.set("1920")
            self._var2.set("1080")
        elif self._val.get() == 2:
            self._var1.set("2048")
            self._var2.set("1080")
        elif self._val.get() == 3:
            self._var1.set("3840")
            self._var2.set("2160")

        try:
            self._width, self._height = int(self._var1.get()), int(self._var2.get())
            try:
                self._small_rooms = int(self._var4.get())
                self._big_rooms = int(self._var5.get())
                self._caveify_val = int(self._var6.get())
            except ValueError:
                self._small_rooms = 0
                self._big_rooms = 0
                try:
                    self._max_rooms = int(self._var3.get())
                except ValueError:
                    self._max_rooms = 0
        except ValueError:
            return

        self._root.destroy()

    def change(self, val):
        # it's for changing check box states
        if val == 0:
            self._advanced_room_settings = not self._advanced_room_settings
        elif val == 1:
            self._advanced_map_settings = not self._advanced_map_settings
            self._val = -1
        elif val == 2:
            self._caveify_on = not self._caveify_on
        elif val == 3:
            self._grid_off = not self._grid_off

        self.place_objects()

    def init_objects(self):
        # initialises all the _labels and so on

        # here we initialise the map size stuff
        self._labels[0] = tk.Label(self._root, text="Map _width:", font=30)
        self._advanced_map_size[0] = tk.Label(self._root, text="Map size:", font=30)
        self._advanced_map_size[1] = tk.Radiobutton(self._root, text="HD", font=30, value=1, variable=self._val)
        self._advanced_map_size[2] = tk.Radiobutton(self._root, text="2k", font=30, value=2, variable=self._val)
        self._advanced_map_size[3] = tk.Radiobutton(self._root, text="4k", font=30, value=3, variable=self._val)
        self._advanced_map_size[4] = tk.Checkbutton(self._root, text="Custom", font=30, command=lambda: self.change(1))
        self._labels[1] = tk.Label(self._root, text="Map _height:", font=30)

        # here we initialise the amount of rooms stuff
        self._labels[2] = tk.Label(self._root, text="Max rooms:", font=30)
        self._labels[3] = tk.Label(self._root, text="Advanced:", font=30)
        self._check_box = tk.Checkbutton(self._root, command=lambda: self.change(0))
        self._labels[4] = tk.Label(self._root, text="Big rooms: ", font=30)
        self._labels[5] = tk.Label(self._root, text="Small rooms: ", font=30)

        self._caveify[0] = tk.Checkbutton(self._root, text="Caveify on:", font=30, command=lambda: self.change(2))
        self._caveify[1] = tk.Label(self._root, text="Degree of Caveification:", font=30)
        self._caveify[2] = tk.Label(self._root, text="*much higher values are recommended for higher resolutions", font=("Comic Sans", "10", "italic"))

        # and here we intialise the entry boxes
        self._entries[0] = tk.Entry(self._root, textvariable=self._var1, font=30)
        self._entries[1] = tk.Entry(self._root, textvariable=self._var2, font=30)
        self._entries[2] = tk.Entry(self._root, textvariable=self._var3, font=30)
        self._entries[3] = tk.Entry(self._root, textvariable=self._var4, font=30)
        self._entries[4] = tk.Entry(self._root, textvariable=self._var5, font=30)
        self._entries[5] = tk.Entry(self._root, textvariable=self._var6, font=30)

        self._other[0] = tk.Checkbutton(self._root, text="Grid OFF", font=30, command=lambda: self.change(3))

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

        self._check_box.place(x=120, y=y2)

        x = 20
        for obj in self._caveify:
            obj.place(x=x, y=y)
            y+=50

        x = 150
        y = 100
        for idx in range(len(self._entries)):
            if idx == 3:
                y += 50
            elif idx == 5:
                y += 50
                x += 100
                self._var6.set('1000')

            self._entries[idx].place(x=x, y=y)
            y += 50

        x = 20
        y += 50
        for obj in self._other:
            obj.place(x=x, y=y)

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
        else:
            self._labels[2].place_forget()
            self._entries[2].place_forget()

        if not self._caveify_on:
            self._caveify[1].place_forget()
            self._caveify[2].place_forget()
            self._entries[5].place_forget()

        self._submit.place(x=150, y=700)
