



MENU = """
-- Recipe and Ingredient App --

Please choose one of these options:

1) Add a new ingredient.
2) See all ingredients.
3) Add a new recipe.
4) See all recipes.
5) Exit.

Your choise: """



def menu():
    while (user_input := input(MENU)) != "5":
        if user_input == "1":
            pass
        elif user_input == "2":
            pass
        elif user_input == "3":
            pass
        elif user_input == "4":
            pass
        else:
            print("Invalid input, try again.")




if __name__ == '__main__':
    menu()