display = [str(x) for x in range(9)]
gameSpace = [' ' for _ in range(9)]
checker = False


def won(letter):
    # check if three of the same symbol are in a line
    # if in a horizontal line
    for row in (gameSpace[i*3:(i+1)*3] for i in range(3)):
        # print(row)
        if all([spot == letter for spot in row]):
            print("3 in horizontal line")
            return True

    # if in vertical line
    for col_idx in range(3):
        col = [gameSpace[col_idx+i*3] for i in range(3)]
        if(all([spot == letter for spot in col])):
            print("3 in a vertical line")
            return True

    # if in a diagnal, if idx%2 is true
    diagnal1 = [gameSpace[i] for i in [0, 4, 8]]
    if(all([spot == letter for spot in diagnal1])):
            print("3 in a left-to-right diagnal")
            return True
    diagnal2 = [gameSpace[i] for i in [2, 4, 6]]
    if(all([spot == letter for spot in diagnal2])):
            print("3 in a right-to-left diagnal")
            return True

    return False


letter = 'x'
while ' ' in gameSpace:

    for row in (display[i*3:(i+1)*3] for i in range(3)):
        print("|" + "|".join(row) + "|")

    spot = int(input(f"Choose where to place your {letter} \n"))

    if gameSpace[spot] == ' ':
        gameSpace[spot] = letter
        for row in (gameSpace[i*3:(i+1)*3] for i in range(3)):
            print("|" + "|".join(row) + "|")

        # after doing a move check if game is over
        if won(letter):
            checker=True
            break

        letter = 'x' if letter == 'o' else 'o'

    else:
        print("That spot is taken")

    print('')

if checker:
    print(f"Well done player {letter} won!")
else:
    print("Looks like a tie")
