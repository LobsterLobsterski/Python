import random


def binary_search(array, start, end, element):
    middle = (end+start)//2

    try:
        if array[middle] == element:
            return middle

        elif element > array[middle]:
            return binary_search(array, middle+1, end, element)
        else:
            return binary_search(array, start, middle-1, element)

    except IndexError:  # if value is out of bounds
        return -1
    except RecursionError:  # if value is not in the array
        return -1


array = set()
for _ in range(1000):
    array.add(random.randint(-500, 500))
array = sorted(list(array))


element = int(input("input value"))
index = binary_search(array, 0, len(array), element)

if index > 0:
    print(f"We've found {element} at index {index} of the array")
else:
    print("We've'nt found the value")
