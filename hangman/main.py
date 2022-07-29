import random
from words import words


def hangman(x):
    word = list(random.choice(words))
    displayed = list("")
    for i in range(len(word)):
        displayed.append("_")

    array_of_guessed = []
    lives = x

    while displayed != word and lives != 0:
        changed = bool(0)
        guess = input("Take a guess \n").lower()

        if guess not in array_of_guessed:
            array_of_guessed.append(guess)
            for i in range(len(word)):
                if word[i] == guess:
                    displayed[i] = guess
                    changed = bool(1)
            if changed:
                print("Nice, you got one!")
            else:
                print("Simply not there...")
                lives -= 1
            print(displayed)

        else:
            print("Alredy guessed that one. Try a different letter.")

    if lives!=0:
        print("Well done you've guessed it!")

    else:
        print("You became the hangman :(")


hangman(5)
