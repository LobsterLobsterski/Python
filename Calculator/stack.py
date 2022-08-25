class Stack:
    def __init__(self):
        self.stack = []
        self.top = -1

    def pop(self):
        if self.is_empty():
            print("stack is empty")
            return

        temp = self.stack[len(self.stack)-1]
        self.stack.pop(self.top)
        self.top -= 1
        return temp

    def push(self, element):
        self.top += 1
        self.stack.append(element)

    def is_empty(self):
        return True if self.top == -1 else False
