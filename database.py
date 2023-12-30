
import sqlite3 as sqlite


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
