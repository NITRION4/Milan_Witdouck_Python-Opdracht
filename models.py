


class Ingredient:
    def __init__(self, ingredient_id, name):
        self.ingredient_id = ingredient_id
        self.name = name

    def __str__(self):
        return f"Id: {self.ingredient_id}, Name: {self.name}"

class Recipe:
    def __init__(self, recipe_id, name, method, rating):
        self.recipe_id = recipe_id
        self.name = name
        self.method = method
        self.rating = rating
        self.ingredients = [] # List of ingredients that belong to my recipe.

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def __str__(self):
        return f"Id: {self.recipe_id}, Name: {self.name}, Method: {self.method}, Rating: {self.rating}, Ingredients: {', '.join(str(ingredient) for ingredient in self.ingredients)}"

