
import database


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
    app = IngredientRecipeApp()

    while (user_input := input(MENU)) != "5":
        if user_input == "1":
            app.add_ingredient()
        elif user_input == "2":
            app.see_all_ingredients()
        elif user_input == "3":
            app.add_recipe()
        elif user_input == "4":
            app.see_all_recipes()
        else:
            print("Invalid input, try again.")



class IngredientRecipeApp:
    def __init__(self):
        self.connection = database.Database()
        self.connection.create_tables()

    # Ingredient methods
    def add_ingredient(self):
        name = input("Ingredient name: ")
        ingredient = self.connection.add_ingredient(name)
        print(f"You succesfully added this ingredient: {ingredient}")

    def see_all_ingredients(self):
        ingredients = self.connection.get_all_ingredients()
        for ingredient in ingredients:
            print(ingredient)

    # Recipe methods
    def add_recipe(self):
        name = input("Recipe name: ")
        method = input("The method how to make this recipe: ")
        #TODO tijdens het adden van een recipe, ook de bijhorende ingredients toevoegen (als deze al bestaan in de database, anders foutmelding)

    def see_all_recipes(self):
        recipes = self.connection.get_all_recipes()
        for recipe in recipes:
            print(recipe)





if __name__ == '__main__':
    menu()