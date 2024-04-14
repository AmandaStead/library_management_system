from faker import Faker
from pymongo import MongoClient
import random
import tkinter as tk
from CRUD import CRUD
from mapReduce import MapReduce


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['library_management']
collection = db['library_collection']

# Instantiate the CRUD class
crud_instance = CRUD()



def generate_user():
    faker = Faker()
    random_name = "User" + str(random.randint(1, 100))
    amount_books = random.randint(1, 15)
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Miami"]
    random_city = random.choice(cities)
    return {"name": random_name, "checked_out_books": amount_books, "city": random_city}


def generate_book():
    adjectives = ['The Secret', 'Hidden', 'Forgotten', 'Lost', 'Mysterious', 'Magical', 'Enchanted']
    nouns = ['Book', 'Tome', 'Scroll', 'Codex', 'Manuscript', 'Chronicle', 'Volume']
    themes = ['Adventure', 'Mystery', 'Fantasy', 'Romance', 'Science Fiction', 'Thriller', 'Historical']
    book_name = f"{random.choice(adjectives)} {random.choice(nouns)} of {random.choice(themes)}"
    return {"name": book_name}


# Function to generate random combined data (user and book info)
def generate_combined_data():
    user_data = generate_user()
    book_data = generate_book()
    combined_data = {
        "user_name": user_data["name"],
        "user_checked_out_books": user_data["checked_out_books"],
        "user_city": user_data["city"],
        "book_name": book_data["name"]
    }
    return combined_data


# Function to insert random data into MongoDB
def insert_random_data():
    random_data = [generate_combined_data() for _ in range(10)]
    collection.insert_many(random_data)
    print("Random data inserted successfully.")
    label.config(text="data imported successfully")


# Functions for CRUD Operation Windows
def open_modify_user_window():
    crud_instance.open_modify_user_window()


def open_delete_user_window():
    crud_instance.open_delete_user_window()


def open_create_user_window():
    crud_instance.open_create_user_window()


def open_find_user_window():
    crud_instance.open_find_user_window()

def open_map_reduce_window():
    root_map_reduce = tk.Tk()
    root_map_reduce.title("Checked Out Books Per City")

    map_reduce_instance = MapReduce(root_map_reduce)

    root_map_reduce.mainloop()




# GUI for Main Screen: generating data, CRUD operations
root = tk.Tk()
root.title("Library Management")

# Set window size for main screen
root.geometry("600x400")  # Width x Height

# Label for insert random data
label = tk.Label(root, text="Click the button to insert random data into MongoDB:")
label.pack()

# Button to insert random data
button_insert = tk.Button(root, text="Insert Random Data", command=insert_random_data)
button_insert.pack()

button_create_user = tk.Button(root, text="Create User", command=open_create_user_window)
button_create_user.pack()

# Button to open the Update Book Amount User
button_modify_user = tk.Button(root, text="Update Book Amount User", command=open_modify_user_window)
button_modify_user.pack()

# Button for delete user
button_delete_user = tk.Button(root, text="Delete User", command=open_delete_user_window)
button_delete_user.pack()

button_find_user = tk.Button(root, text="Find User", command=open_find_user_window)
button_find_user.pack()

button_map_reduce = tk.Button(root, text="Checked Out Books Per City", command=open_map_reduce_window)
button_map_reduce.pack()


root.mainloop()
