
import sqlite3 as sqlite
from models import Ingredient, Recipe


CREATE_INGREDIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT
);
"""

CREATE_RECIPES_TABLE = """
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    method TEXT
);
"""


# Ingredient methods:
INSERT_INGREDIENT = "INSERT INTO ingredients (name) VALUES (?);"

GET_ALL_INGREDIENTS = "SELECT * FROM ingredients;"


# Recipe methods:
INSERT_RECIPE = "INSERT INTO recipes (name, method) VALUES (?,?);"

GET_ALL_RECIPES = "SELECT * FROM recipes;"



class Database:
    def __init__(self):
        self.connection = sqlite.connect("data.db") #TODO ervoor zorgen dat data.db ergens anders wordt opgeslaan. Nu even .gitignore aangepast zodat het niet commit wordt.
        self.cursor = self.connection.cursor()

    def create_tables(self):
        with self.connection:
            self.connection.execute(CREATE_INGREDIENTS_TABLE)
            self.connection.execute(CREATE_RECIPES_TABLE)

    #Ingredient methods:
    def add_ingredient(self, name):
        with self.connection:
            cursor = self.connection.execute(INSERT_INGREDIENT, (name,)) # (name,) --> is zo geschreven omdat het eigenlijk een tuple is die hij nodig heeft.
            return Ingredient(name)

    def get_all_ingredients(self):
        with self.connection:
            rows = self.connection.execute(GET_ALL_INGREDIENTS).fetchall()
            return [Ingredient(row[0]) for row in rows]


    # Recipe methods:
    def add_recipe(self, name, method):
        with self.connection:
            cursor = self.connection.execute(INSERT_RECIPE, (name, method))
            return Recipe(name, method)
            #TODO ervoor zorgen dat ik ook ingredients direct kan toevoegen aan mijn recipe wanneer ik hem aanmaak.

    def get_all_recipes(self):
        with self.connection:
            rows = self.connection.execute(GET_ALL_RECIPES).fetchall()
            return [Recipe(row[0], row[1]) for row in rows]


























