import tkinter as tk

"""
Not gonna sugar coat it, i hate tkinter. 
Simple menu class for handling all all of the labels,
entry boxes e.t.c. 
"""


class Menu:
    def __init__(self, root):
        self.root = root
        self.width, self.height = 0, 0
        self.max_rooms = 0
        self.advanced_room_settings = False
        self.advanced_map_settings = False
        self.caveify_on = False
        self.caveify_val = 1000
        self.small_rooms = 0
        self.big_rooms = 0
        self.val = -1
        self.advanced_map_size = [0 for _ in range(5)]
        self.labels = [0 for _ in range(6)]
        self.entries = [0 for _ in range(6)]
        self.caveify = [0 for _ in range(3)]
        self.check_box = ...
        self.submit = tk.Button(self.root, text="Submit", font=30, command=lambda: self.submit_click())

        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()
        self.var4 = tk.StringVar()
        self.var5 = tk.StringVar()
        self.var6 = tk.StringVar()

        self.init_objects()

    def submit_click(self):
        # saves the inputted values and exits the tkinter loop
        if self.val == 0:
            self.var1.set("1920")
            self.var2.set("1080")
        elif self.val == 1:
            self.var1.set("2048")
            self.var2.set("1080")
        elif self.val == 2:
            self.var1.set("3840")
            self.var2.set("2160")

        try:
            self.width, self.height = int(self.var1.get()), int(self.var2.get())
            self.max_rooms = int(self.var3.get())
            try:
                self.small_rooms = int(self.var4.get())
                self.big_rooms = int(self.var5.get())
                self.caveify_val = int(self.var6.get())
            except ValueError:
                self.small_rooms = 0
                self.big_rooms = 0
        except ValueError:
            return

        # print(f'{(self.width, self.height, self.max_rooms, self.small_rooms, self.big_rooms)=}')
        self.root.destroy()

    def change(self, val):
        # it's for changing check box states
        if val == 0:
            self.advanced_room_settings = not self.advanced_room_settings
        if val == 1:
            self.advanced_map_settings = not self.advanced_map_settings
            self.val = -1
        if val == 2:
            self.caveify_on = not self.caveify_on

        self.place_objects()

    def clicked(self, val):
        # to check which radio button is on
        self.val = val

    def init_objects(self):
        # initialises all the labels and so on

        # here we initialise the map size stuff
        self.labels[0] = tk.Label(self.root, text="Map width:", font=30)
        self.advanced_map_size[0] = tk.Label(self.root, text="Map size:", font=30)
        self.advanced_map_size[1] = tk.Radiobutton(self.root, text="HD", font=30, value=0, command=lambda: self.clicked(0))
        self.advanced_map_size[2] = tk.Radiobutton(self.root, text="2k", font=30, value=1, command=lambda: self.clicked(1))
        self.advanced_map_size[3] = tk.Radiobutton(self.root, text="4k", font=30, value=2, command=lambda: self.clicked(2))
        self.advanced_map_size[4] = tk.Checkbutton(self.root, text="Custom", font=30, command=lambda: self.change(1))
        self.labels[1] = tk.Label(self.root, text="Map height:", font=30)

        # here we initialise the amount of rooms stuff
        self.labels[2] = tk.Label(self.root, text="Max rooms:", font=30)
        self.labels[3] = tk.Label(self.root, text="Advanced:", font=30)
        self.check_box = tk.Checkbutton(self.root, command=lambda: self.change(0))
        self.labels[4] = tk.Label(self.root, text="Big rooms: ", font=30)
        self.labels[5] = tk.Label(self.root, text="Small rooms: ", font=30)

        self.caveify[0] = tk.Checkbutton(self.root, text="Caveify on:", font=30, command=lambda: self.change(2))
        self.caveify[1] = tk.Label(self.root, text="Degree of Caveification:", font=30)
        self.caveify[2] = tk.Label(self.root, text="*much higher values are recommended for higher resolutions", font=("Comic Sans", "10", "italic"))

        # and here we intialise the entry boxes
        self.entries[0] = tk.Entry(self.root, textvariable=self.var1, font=30)
        self.entries[1] = tk.Entry(self.root, textvariable=self.var2, font=30)
        self.entries[2] = tk.Entry(self.root, textvariable=self.var3, font=30)
        self.entries[3] = tk.Entry(self.root, textvariable=self.var4, font=30)
        self.entries[4] = tk.Entry(self.root, textvariable=self.var5, font=30)
        self.entries[5] = tk.Entry(self.root, textvariable=self.var6, font=30)

        self.place_objects()

    def place_objects(self):
        # takes all the initialised 'objects' and places them on the screens

        x, y = 40, 50
        for idx in range(len(self.advanced_map_size)):
            if idx == 0:
                self.advanced_map_size[idx].place(x=20, y=50)
            else:
                self.advanced_map_size[idx].place(x=x, y=y)
            x += 80

        y = 100
        x = 20
        for idx in range(len(self.labels)):
            if idx == 3:
                y2 = y
            self.labels[idx].place(x=x, y=y)
            y += 50

        self.check_box.place(x=120, y=y2)

        x = 20
        for obj in self.caveify:
            obj.place(x=x, y=y)
            y+=50

        x = 150
        y = 100
        for idx in range(len(self.entries)):
            if idx == 3:
                y += 50
            elif idx == 5:
                y += 50
                x += 100
                self.var6.set('1000')

            self.entries[idx].place(x=x, y=y)
            y += 50

        # if some check boxes are checked we have to 'forget' to place some things
        if not self.advanced_map_settings:
            self.labels[0].place_forget()
            self.labels[1].place_forget()
            self.entries[0].place_forget()
            self.entries[1].place_forget()
        else:
            for idx in range(len(self.advanced_map_size)-1):
                self.advanced_map_size[idx].place_forget()

        if not self.advanced_room_settings:
            self.labels[4].place_forget()
            self.labels[5].place_forget()
            self.entries[3].place_forget()
            self.entries[4].place_forget()

        if not self.caveify_on:
            self.caveify[1].place_forget()
            self.caveify[2].place_forget()
            self.entries[5].place_forget()

        self.submit.place(x=150, y=600)
