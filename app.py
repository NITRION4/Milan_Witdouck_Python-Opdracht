
import database


MENU = """
-- Recipe and Ingredient App --

Please choose one of these options:

1) Add a new ingredient.
2) See all ingredients.
3) Add a new recipe.
4) See all recipes.
5) Exit.

Your choice: """



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
        name = input("Ingredient name: ").lower()
        ingredient = self.connection.add_ingredient(name)
        print(f"You successfully added this ingredient: {ingredient}")

    def see_all_ingredients(self):
        ingredients = self.connection.get_all_ingredients()
        for ingredient in ingredients:
            print(ingredient)

    # Recipe methods
    def add_recipe(self):
        name = input("Recipe name: ").lower()
        method = input("The method how to make this recipe: ")
        rating = int(input("Give this recipe a score from 0-100: "))

        ingredients = []
        while (input("Do you want to add an ingredient to this recipe? (y/n): ").lower()) == "y":
            ingredient_name = input("Enter ingredient name: ")
            ingredient = self.connection.get_ingredient_by_name(ingredient_name)
            if ingredient:
                ingredients.append(ingredient.ingredient_id)
            else:
                print(f"Ingredient '{ingredient_name}' doesn't exist. Add it first.")

        recipe = self.connection.add_recipe(name, method, rating, ingredients)
        print(f"You successfully added this recipe: {recipe}")

    def see_all_recipes(self):
        recipes = self.connection.get_all_recipes()
        for recipe in recipes:
            print(recipe)





if __name__ == '__main__':
    menu()