


class Ingredient:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Name: {self.name}"

class Recipe:
    def __init__(self, name, method):
        self.name = name
        self.method = method
        self.ingredients = [] # List of ingredients that belong to my recipe.

    def __str__(self):
        return f"Name: {self.name}, Method: {self.method}, Ingredients: " #TODO alle ingredients ook afdrukken die bij deze recipe horen.


