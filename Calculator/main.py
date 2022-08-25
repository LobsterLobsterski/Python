import operator
import tkinter as tk

from stack import Stack

#####################################################
# Code made by Tomasz Potoczko as one of lower
# complexity projects. This is an implementation of
# a simple calculator using tkinter GUI, stacks and
# infix to postfix conversion. Feeling real proud
# of it even though many might find it trivial.
#####################################################


class Calculator:
    def __init__(self, master):
        self.master = master  # master window
        self.brackets = 0  # used to make sure brackets are placed correctly
        self.input = tk.StringVar()
        self.result = tk.StringVar()
        self.input.set("")
        self.result.set("")
        self.create_buttons()

    @staticmethod
    def calculate(prefix):
        ops = {'+': operator.add, '-': operator.sub, '*': operator.mul,
               '/': operator.truediv, '%': operator.mod, '^': operator.pow
               }
        operands = Stack()

        for val in prefix:
            try:
                operands.push(int(val))

            except ValueError:
                operand2 = operands.pop()
                operand1 = operands.pop()
                operands.push(ops[val](operand1, operand2))

        last = operands.pop()
        # this limits the number of decimal points to 10
        last = int(last * (10 ** 10))
        last = last / (10 ** 10)
        # print(f"last {last}")

        return last

    @staticmethod
    def turn_postfix(initial_array):
        postfix = []
        operators = Stack()
        for val in initial_array:
            try:
                postfix.append(str(int(val)))
            except ValueError:
                # RULE 1: we pop if we have a single operator enclosed in brackets
                # check last three values of operators stack and if the first is ( and third is ) then we need to pop them
                if len(operators.stack) > 2:
                    last_3 = [operators.stack[operators.top - i] for i in range(0, 3)]
                    if last_3[0] in ["(", ")"] and last_3[2] in ["(", ")"]:
                        operators.pop()
                        postfix.append(operators.pop())
                        operators.pop()

                # RULE 2: we pop if the next value we were to push were to be of equal or lower priority
                # we need to loop through the whole stack to make sure we are popping until we can push
                if len(operators.stack) > 1:
                    for i in range(len(operators.stack) - 1, -1, -1):
                        prev_operator = operators.stack[operators.top]
                        # print(f"val: {val}, prev_operator: {prev_operator}")
                        if val in ["+", "-"] and prev_operator in ["+", "-", "*", "/", "^"] or val in ["*", "/"] and \
                                prev_operator in ["*", "/", "^"] or val == "^" and prev_operator == "^":
                            postfix.append(operators.pop())
                    operators.push(val)

                else:
                    operators.push(val)

        # and at the end we need to put all thats left in the stack into the prefix
        for idx in range(len(operators.stack) - 1, -1, -1):
            if operators.stack[idx] not in ["(", ")"]:
                postfix.append(operators.pop())
            else:
                operators.pop()

        # print(f"postfix: {postfix}")
        return postfix

    def turn_to_array(self, string_equation):
        digit_counter = 0
        array = []
        for idx, element in enumerate(string_equation):
            if element in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                digit_counter += 1
            else:
                # print(f"integer: {string_equation[idx-digit_counter: idx]}")
                array.append(string_equation[idx - digit_counter: idx])
                array.append(element)
                digit_counter = 0

        if digit_counter != 0:
            # print(f"integer: {string_equation[len(string_equation)-digit_counter:]}")
            array.append(string_equation[len(string_equation) - digit_counter:])

        array = list(filter(lambda item: item != '', array))

        postfix = self.turn_postfix(array)

        self.result.set('= ' + str(self.calculate(postfix)))

    def add_to_input(self, var, type_of_var, back=False):
        val = self.input.get()

        if type_of_var == 2:
            self.turn_to_array(val)
            return

        # if we adding values
        if not back:
            # if an integer
            if type_of_var == 0:
                # print("OPERAND")
                self.input.set(val + var)
                return
            # if an operator
            elif type_of_var == 1:
                # print("OPERATOR")
                # we can't place an operator first unless its a -, or ( )
                if var not in ["-", "(", ")", "( )"]:
                    # if its a +, *, /, or ^ we need to check if the previous one inputted is an int then we can
                    # add it to the end
                    idx = 0
                    try:
                        idx = len(val) - 1
                        if idx < 0:
                            raise IndexError
                    except IndexError:
                        return

                    if val[idx] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ")"]:
                        # print("previous input is an int, placing")
                        self.input.set(val + var)
                        return

                    # print("previous input not an int")
                    return

                # var is a -
                if var != "( )":
                    # print(var)
                    self.input.set(val + var)
                    return

                # var is a bracket
                # if previous input is none or operator then open, if previous is an integer close
                if len(val) == 0 or val[len(val) - 1] in ["+", "-", "*", "/", "^", "√", "("] or self.brackets == 0:
                    var = '('
                    self.brackets += 1
                    # print(f"opened one. Currently: {self.brackets }")
                elif len(val) > 0 and val[len(val) - 1] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                                                            ")"] and self.brackets > 0:
                    var = ')'
                    self.brackets -= 1
                    # print(f"closed one. Currently: {self.brackets }")

                self.input.set(val + var)
                return

        # if we removing values
        try:
            if val[len(val) - 1] == '(':
                self.brackets -= 1
            elif val[len(val) - 1] == ')':
                self.brackets += 1

            self.input.set(val[:len(val) - 1])
        except IndexError:
            pass

    def create_buttons(self):
        input_label = tk.Label(root, textvariable=self.input, font=40)
        result_label = tk.Label(root, textvariable=self.result, font=40)
        buttons_names = (("1", lambda: self.add_to_input('1', 0)), ("2", lambda: self.add_to_input('2', 0)),
                         ("3", lambda: self.add_to_input('3', 0)), ("4", lambda: self.add_to_input('4', 0)),
                         ("5", lambda: self.add_to_input('5', 0)), ("6", lambda: self.add_to_input('6', 0)),
                         ("7", lambda: self.add_to_input('7', 0)), ("8", lambda: self.add_to_input('8', 0)),
                         ("9", lambda: self.add_to_input('9', 0)), ("0", lambda: self.add_to_input('0', 0)),
                         ("+", lambda: self.add_to_input('+', 1)), ("-", lambda: self.add_to_input('-', 1)),
                         ("*", lambda: self.add_to_input('*', 1)), ("/", lambda: self.add_to_input('/', 1)),
                         ("a^b", lambda: self.add_to_input('^', 1)), ("( )", lambda: self.add_to_input('( )', 1)),
                         ("back", lambda: self.add_to_input('', 1, True)), ("=", lambda: self.add_to_input('', 2)))

        buttons = []
        for i in buttons_names:
            buttons.append(tk.Button(root, command=i[1], text=i[0], height=4, width=6))

        row = 0
        col = 80
        input_label.place(relx=0, rely=0)
        result_label.place(relx=0, rely=0.06)
        for i, but in enumerate(buttons):
            but.place(x=row, y=col)
            if i == 9:
                col += 80

            if row < 250:
                row += 80
            else:
                row = 0
                col += 80


if __name__ == '__main__':
    root = tk.Tk(className="Simple Calculator app")
    root.geometry("400x600")
    root.minsize(400, 600)
    root.maxsize(400, 600)
    root.configure(bg='#ADD8E6')

    calc = Calculator(root)

    root.mainloop()
