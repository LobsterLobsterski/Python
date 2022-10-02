"""
File holding different room classes to creating various room shapes
"""


class Rect:
    def __init__(self, x, y, width, height, size_mod):
        self.x1 = x
        self.y1 = y
        self.x2 = x + height*size_mod
        self.y2 = y + width*size_mod

    def __str__(self):
        return f"Rect: (x1= {self.x1}, y1= {self.y1}, x2= {self.x2}, y2= {self.y2})"

    def print_all(self):
        print(f"{self.x1=}\n{self.y1=}\n{self.x2=}\n{self.y2=}\n")
