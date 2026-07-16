import random
print('Winning rules of the game FIRE WATER GRASS are:\n'
      + "FIRE vs WATER -> WATER wins \n"
      + "FIRE vs GRASS -> FIRE wins \n"
      + "WATER vs GRASS -> GRASS wins \n")

while True:

    print("Enter your choice \n 1 - FIRE \n 2 - WATER \n 3 - GRASS \n")

    choice = int(input("Enter your choice: "))
    while choice > 3 or choice < 1:
        choice = int(input('Enter a valid choice please ☺: '))
    if choice == 1:
        choice_name = 'FIRE'
    elif choice == 2:
        choice_name = 'WATER'
    else:
        choice_name = 'GRASS'
    print('User choice is:', choice_name)
    print("Now it's Computer's Turn...")
    comp_choice = random.randint(1, 3)
    if comp_choice == 1:
        comp_choice_name = 'FIRE'
    elif comp_choice == 2:
        comp_choice_name = 'WATER'
    else:
        comp_choice_name = 'GRASS'

    print("Computer choice is:", comp_choice_name)
    print(choice_name, 'vs', comp_choice_name)

    if choice == comp_choice:
        result = "DRAW"
    elif (choice == 1 and comp_choice == 2) or (comp_choice == 1 and choice == 2):
        result = 'WATER'
    elif (choice == 1 and comp_choice == 3) or (comp_choice == 1 and choice == 3):
        result = 'FIRE'
    elif (choice == 2 and comp_choice == 3) or (comp_choice == 2 and choice == 3):
        result = 'GRASS'

    if result == "DRAW":
        print("<== It's a tie! ==>")
    elif result == choice_name:
        print("<== User wins! ==>")
    else:
        print("<== Computer wins! ==>")

    print("Do you want to play again? (Y/N)")
    ans = input().lower()
    if ans == 'n':
        break
print("Thanks for playing!")
