
import sqlite3 as sqlite
from models import Ingredient, Recipe
import csv
import pandas as pd
import openpyxl  # Needed for the excel export.
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DATABASE_LOCATION = config.get('Database', 'location', fallback='data.db')



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
    method TEXT,
    rating INTEGER
);
"""

CREATE_RECIPE_INGREDIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER,
    ingredient_id INTEGER,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);
"""


# Ingredient methods:
INSERT_INGREDIENT = "INSERT INTO ingredients (name) VALUES (?);"

GET_ALL_INGREDIENTS = "SELECT * FROM ingredients;"

GET_INGREDIENT_BY_NAME = "SELECT * FROM ingredients WHERE name = ?;"


# Recipe methods:
INSERT_RECIPE = "INSERT INTO recipes (name, method, rating) VALUES (?,?,?);"

GET_ALL_RECIPES = "SELECT * FROM recipes;"

GET_RECIPE_BY_NAME = "SELECT * FROM recipes WHERE name = ?;"

# Recipe ingredient methods:
INSERT_RECIPE_INGREDIENT = "INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?,?);"

GET_RECIPE_INGREDIENTS = """
SELECT ingredients.id, ingredients.name
FROM recipe_ingredients
JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id
WHERE recipe_ingredients.recipe_id = ?;
"""

class Database:
    def __init__(self):
        self.connection = sqlite.connect(DATABASE_LOCATION)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        with self.connection:
            self.connection.execute(CREATE_INGREDIENTS_TABLE)
            self.connection.execute(CREATE_RECIPES_TABLE)
            self.connection.execute(CREATE_RECIPE_INGREDIENTS_TABLE)

    #Ingredient methods:
    def add_ingredient(self, name):
        with self.connection:
            cursor = self.connection.execute(INSERT_INGREDIENT, (name,)) # (name,) --> is written like this because it's actually a tuple.
            ingredient_id = cursor.lastrowid
            return Ingredient(ingredient_id, name)

    def get_all_ingredients(self):
        with self.connection:
            rows = self.connection.execute(GET_ALL_INGREDIENTS).fetchall()
            return [Ingredient(row[0], row[1]) for row in rows]

    def get_ingredient_by_name(self, name):
        with self.connection:
            row = self.connection.execute(GET_INGREDIENT_BY_NAME, (name,)).fetchone()
            if row:
                return Ingredient(row[0], row[1])
            return None

    def get_ingredient_by_id(self, ingredient_id): # So I can use the add_recipe method and instantly add ingredients to the recipe
        with self.connection:
            row = self.connection.execute("SELECT * FROM ingredients WHERE id = ?", (ingredient_id,)).fetchone()
            if row:
                return Ingredient(row[0], row[1])
            return None

    def update_ingredient(self, ingredient_id, new_name):
        with self.connection:
            self.connection.execute("UPDATE ingredients SET name = ? WHERE id = ?;", (new_name, ingredient_id))

    # Recipe methods:
    def add_recipe(self, name, method, rating, ingredients):
        with self.connection:
            cursor = self.connection.execute(INSERT_RECIPE, (name, method, rating))
            recipe_id = cursor.lastrowid

            recipe = Recipe(recipe_id, name, method, rating)
            for ingredient_id in ingredients:
                recipe.add_ingredient(self.get_ingredient_by_id(ingredient_id))

            return recipe

    def get_all_recipes(self):
        with self.connection:
            rows = self.connection.execute(GET_ALL_RECIPES).fetchall()
            return [Recipe(row[0], row[1], row[2], row[3]) for row in rows]

    def get_recipe_by_name(self, name):
        with self.connection:
            row = self.connection.execute(GET_RECIPE_BY_NAME, (name,)).fetchone()
            if row:
                return Recipe(row[0], row[1], row[2], row[3])
            return None

    def get_recipe_ingredients(self, recipe_id):
        with self.connection:
            rows = self.connection.execute(GET_RECIPE_INGREDIENTS, (recipe_id,)).fetchall()
            return [Ingredient(row[0], row[1]) for row in rows]

    def update_recipe(self, recipe_id, new_name, new_method, new_rating, new_ingredients):
        with self.connection:
            self.connection.execute("UPDATE recipes SET name = ?, method = ?, rating = ? WHERE id = ?", (new_name, new_method, new_rating, recipe_id))

            # Remove links between recipe and his ingredients.
            self.connection.execute("DELETE FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,))

            # Add the new ingredients to the recipe
            self.connection.executemany("INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?, ?)", [(recipe_id, ingredient_id) for ingredient_id in new_ingredients])

    # Recipe ingredients methods:
    def add_recipe_ingredients(self, recipe_id, ingredient_ids):
        with self.connection:
            self.connection.executemany(INSERT_RECIPE_INGREDIENT, [(recipe_id, ingredient_id) for ingredient_id in ingredient_ids])





    # Export methods:
    def export_to_csv(self, output_csv):
        cursor = self.cursor

        # These queries are used to get the correct data
        query_ingredients = "SELECT * FROM ingredients;"
        query_recipes = "SELECT * FROM recipes;"
        query_recipe_ingredients = "SELECT * FROM recipe_ingredients;"

        with open(output_csv, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # To make the column header for Ingredients
            csv_writer.writerow(["Ingredients"])
            cursor.execute(query_ingredients)
            csv_writer.writerow([description[0] for description in cursor.description])

            # Add the data
            for row in cursor.execute(query_ingredients):
                csv_writer.writerow(row)

            # To make the column header for Recipes
            csv_writer.writerow([])  # Add a blank line between tables
            csv_writer.writerow(["Recipes"])
            cursor.execute(query_recipes)
            csv_writer.writerow([description[0] for description in cursor.description])

            for row in cursor.execute(query_recipes):
                csv_writer.writerow(row)

            # To make the column header for Recipe Ingredients
            csv_writer.writerow([])  # Add a blank line between tables
            csv_writer.writerow(["Recipe Ingredients"])
            cursor.execute(query_recipe_ingredients)
            csv_writer.writerow([description[0] for description in cursor.description])

            for row in cursor.execute(query_recipe_ingredients):
                csv_writer.writerow(row)


    def export_to_excel(self, output_excel):
        # These queries are used to get the correct data
        query_ingredients = "SELECT * FROM ingredients;"
        query_recipes = "SELECT * FROM recipes;"
        query_recipe_ingredients = "SELECT * FROM recipe_ingredients;"

        # Use of pandas for the data
        ingredients_df = pd.read_sql_query(query_ingredients, self.connection)
        recipes_df = pd.read_sql_query(query_recipes, self.connection)
        recipe_ingredients_df = pd.read_sql_query(query_recipe_ingredients, self.connection)

        with pd.ExcelWriter(output_excel) as writer:
            ingredients_df.to_excel(writer, sheet_name='Ingredients', index=False)
            recipes_df.to_excel(writer, sheet_name='Recipes', index=False)
            recipe_ingredients_df.to_excel(writer, sheet_name='RecipeIngredients', index=False)



