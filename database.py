# database.py
import sqlite3

conn = sqlite3.connect("restaurants.db")
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        location TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        restaurant_id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        location TEXT,
        rating REAL
    )
    """)
    conn.commit()

def add_user(user_id, username, location):
    cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", (user_id, username, location))
    conn.commit()

def get_user_location(user_id):
    cursor.execute("SELECT location FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def add_restaurant(restaurant):
    cursor.execute("""
    INSERT OR REPLACE INTO restaurants (restaurant_id, name, category, location, rating)
    VALUES (?, ?, ?, ?, ?)
    """, (
        restaurant['id'],
        restaurant['name'],
        restaurant['category'],
        restaurant['location'],
        restaurant['rating']
    ))
    conn.commit()
