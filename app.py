
import database


MENU = """
-- Recipe and Ingredient App --

Please choose one of these options:

* Ingredient methods *
1) Add a new ingredient.
2) See all ingredients.
3) Find an ingredient by name.
4) Update an ingredient.

* Recipe methods *
5) Add a new recipe.
6) See all recipes.
7) Find a recipe by name.
8) Find ingredients and method for a recipe.
9) Update a recipe.

* Export methods *
10) Export data to CSV.
11) Export data to Excel.

12) Exit.

Your choice: """



def menu():
    app = IngredientRecipeApp()

    while (user_input := input(MENU)) != "12":
        if user_input == "1":
            app.add_ingredient()
        elif user_input == "2":
            app.see_all_ingredients()
        elif user_input == "3":
            app.find_ingredient()
        elif user_input == "4":
            app.update_ingredient()
        elif user_input == "5":
            app.add_recipe()
        elif user_input == "6":
            app.see_all_recipes()
        elif user_input == "7":
            app.find_recipe()
        elif user_input == "8":
            app.find_recipe_ingredients()
        elif user_input == "9":
            app.update_recipe()
        elif user_input == "10":
            app.connection.export_to_csv("exported_IngredientRecipeApp_data.csv")
            print("Data successfully exported to 'exported_IngredientRecipeApp_data.csv'")
        elif user_input == "11":
            app.connection.export_to_excel("exported_IngredientRecipeApp_data.xlsx")
            print("Data successfully exported to 'exported_IngredientRecipeApp_data.xlsx'")
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
        print(f"You successfully added this ingredient: {ingredient}")

    def see_all_ingredients(self):
        ingredients = self.connection.get_all_ingredients()
        for ingredient in ingredients:
            print(ingredient)

    def find_ingredient(self):
        name = input("Ingredient name to find: ")
        ingredient = self.connection.get_ingredient_by_name(name)
        if ingredient:
            print(f"Successfully found this ingredient: "
                  f"{ingredient}")
        else:
            print(f"Ingredient '{name}' not found.")


    # Recipe methods
    def add_recipe(self):
        name = input("Recipe name: ")
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
        self.connection.add_recipe_ingredients(recipe.recipe_id, ingredients)
        print(f"You successfully added this recipe: {recipe}")

    def see_all_recipes(self):
        recipes = self.connection.get_all_recipes()
        for recipe in recipes:
            print(f"Id: {recipe.recipe_id}, Name: {recipe.name}, Method: {recipe.method}, Rating: {recipe.rating}")

    def find_recipe(self):
        name = input("Recipe name to find: ")
        recipe = self.connection.get_recipe_by_name(name)
        if recipe:
            print(f"Id: {recipe.recipe_id}, Name: {recipe.name}, Method: {recipe.method}, Rating: {recipe.rating}")
        else:
            print(f"Recipe '{name}' not found.")

    def find_recipe_ingredients(self):
        name = input("Enter recipe name to find ingredients: ")
        recipe = self.connection.get_recipe_by_name(name)
        if recipe:
            recipe_id = recipe.recipe_id
            ingredients = self.connection.get_recipe_ingredients(recipe_id)

            print(f"Method for {name}: {recipe.method}")
            print(f"Ingredients for {name}:")
            for ingredient in ingredients:
                print(ingredient)
        else:
            print(f"Recipe '{name}' not found.")


    def update_ingredient(self):
        ingredient_id = input("Enter the ID of the ingredient you want to update: ")
        new_name = input("Give a new name to the ingredient: ")
        self.connection.update_ingredient(ingredient_id, new_name)
        print("Ingredient updated successfully!")

    def update_recipe(self):
        recipe_id = input("Enter the ID of the recipe you want to update: ")
        new_name = input("Give a new name to the recipe: ")
        new_method = input("Enter the new method for the recipe: ")
        new_rating = int(input("Enter the new rating for the recipe (0-100): "))

        new_ingredients = []
        while (input("Do you want to add an ingredient to the recipe? (y/n): ").lower()) == "y":
            ingredient_name = input("Enter ingredient name: ")
            ingredient = self.connection.get_ingredient_by_name(ingredient_name)
            if ingredient:
                new_ingredients.append(ingredient.ingredient_id)
            else:
                print(f"Ingredient '{ingredient_name}' not found. Please add it first.")

        self.connection.update_recipe(recipe_id, new_name, new_method, new_rating, new_ingredients)
        print("Recipe updated successfully.")



if __name__ == '__main__':
    menu()