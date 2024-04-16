from faker import Faker
from pymongo import MongoClient
import random
import tkinter as tk

from utils import generate_book


class CRUD:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['library_management']
        self.collection = self.db['library_collection']
        self.error_label = None
        self.update_error_label = None

    def delete_user(self, username):
        result = self.collection.delete_one({"user_name": username})
        if result.deleted_count == 1:
            print("User Deleted")
            return True
        else:
            print("User not found.")
            return False

    def create_user(self, user_name, checked_out_books, city):
        books = [generate_book()["name"] for _ in range(checked_out_books)]
        new_user = {
            "user_name": user_name,
            "user_checked_out_books": checked_out_books,
            "user_city": city,
            "books": books
        }

        try:
            self.collection.insert_one(new_user)
            print("User Created")
            self.error_label.config(text="User created successfully", fg="green")
            return True
        except ValueError:
            self.error_label.config(text="Error: Checked Out Books must be a non-negative integer", fg="red")
            return False
        except Exception as e:
            print("Error creating user:", e)
            self.error_label.config(text=f"Error creating user: {e}", fg="red")
            return False

    def find_user(self, username):
        user_data = self.collection.find_one({"user_name": username})
        if user_data:
            return user_data
        else:
            print("User not found.")
            return None

    def update_checked_out_books(self, username, new_amount):
        user_data = self.find_user(username)

        if user_data:
            try:
                new_amount = int(new_amount)
                self.collection.update_one({"user_name": username}, {"$set": {"user_checked_out_books": new_amount}})
                print("Book amount checked out updated successfully.")

                updated_books = [generate_book()["name"] for _ in range(new_amount)]
                self.collection.update_one({"user_name": username}, {"$set": {"books": updated_books}})

                self.update_error_label.config(text="Update book amount successful", fg="black")
            except ValueError:
                self.update_error_label.config(text="New Book Amount must be an integer", fg="red")
        else:
            print("User not Found.")
            self.update_error_label.config(text="User not Found", fg="red")

    def open_modify_user_window(self):
        # Function to open modify user window
        modify_user_window = tk.Toplevel()
        modify_user_window.title("Modify User")

        modify_user_window.geometry("400x300")

        # Username Label and Entry
        username_label = tk.Label(modify_user_window, text="Username:")
        username_label.pack()

        self.username_entry = tk.Entry(modify_user_window)
        self.username_entry.pack()

        # New Book Amount Label and Entry
        new_amount_label = tk.Label(modify_user_window, text="New Book Amount Checked Out:")
        new_amount_label.pack()

        self.new_amount_entry = tk.Entry(modify_user_window)
        self.new_amount_entry.pack()

        self.update_error_label = tk.Label(modify_user_window, text="", fg="red")  # update_error_label
        self.update_error_label.pack()

        # Button to Update Book Amount Checked Out
        update_button = tk.Button(modify_user_window, text="Update Book Amount Checked Out",
                                  command=self.update_checked_out_books_wrapper)

        # Button to Update Book Amount Checked Out
        delete_user_button = tk.Button(modify_user_window, text="Delete User",
                                       command=self.delete_user)
        update_button.pack()

        global label
        label = tk.Label(modify_user_window, text="")
        label.pack()

    def open_find_user_window(self):
        find_user_window = tk.Toplevel()
        find_user_window.title("Find User")

        username_label = tk.Label(find_user_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(find_user_window)
        username_entry.pack()

        text_area = tk.Text(find_user_window, height=10, width=50)
        text_area.pack()

        not_found_label = tk.Label(find_user_window, text="", fg="red")
        not_found_label.pack()

        def find_user():
            username = username_entry.get()
            user_data = self.find_user(username)
            if user_data:
                text_area.delete('1.0', tk.END)
                for key, value in user_data.items():
                    text_area.insert(tk.END, f"{key}: {value}\n")
            else:
                not_found_label.config(text="User not found")

        find_button = tk.Button(find_user_window, text="Find User", command=find_user)
        find_button.pack()

    def open_delete_user_window(self):
        delete_user_window = tk.Toplevel()
        delete_user_window.title("Delete User")

        delete_user_window.geometry("400x300")

        username_label = tk.Label(delete_user_window, text="Username:")
        username_label.pack()

        username_entry = tk.Entry(delete_user_window)
        username_entry.pack()

        result_label = tk.Label(delete_user_window, text="", fg="red")
        result_label.pack()

        # Button to Delete User
        def delete_user():
            username = username_entry.get()
            deleted = self.delete_user(username)
            if deleted:
                result_label.config(text="User deleted successfully", fg="green")
            else:
                result_label.config(text="User not found", fg="red")

        delete_button = tk.Button(delete_user_window, text="Delete User", command=delete_user)
        delete_button.pack()

    def open_create_user_window(self):
        create_user_window = tk.Toplevel()
        create_user_window.title("Create User")

        create_user_window.geometry("400x300")

        username_label = tk.Label(create_user_window, text="Username:")
        username_label.pack()

        username_entry = tk.Entry(create_user_window)
        username_entry.pack()

        checked_out_books_label = tk.Label(create_user_window, text="Checked Out Books:")
        checked_out_books_label.pack()

        checked_out_books_entry = tk.Entry(create_user_window)
        checked_out_books_entry.pack()

        city_label = tk.Label(create_user_window, text="City:")
        city_label.pack()

        city_entry = tk.Entry(create_user_window)
        city_entry.pack()

        self.error_label = tk.Label(create_user_window, text="", fg="red")
        self.error_label.pack()

        def create_user(error_label):
            user_name = username_entry.get()
            checked_out_books_str = checked_out_books_entry.get()
            city = city_entry.get()

            try:
                checked_out_books = int(checked_out_books_str)
                if checked_out_books < 0: raise ValueError(
                    "Checked Out Books must be a non-negative integer")
                self.create_user(user_name, checked_out_books, city)
                error_label.config(text="User created successfully", fg="green")
            except ValueError as e:
                error_label.config(text="Please enter valid integer", fg="red")

        create_button = tk.Button(create_user_window, text="Create User", command=lambda: create_user(self.error_label))
        create_button.pack()

    def update_checked_out_books_wrapper(self):
        # Wrapper function to get entry values and call update_checked_out_books
        username = self.username_entry.get()
        new_amount_str = self.new_amount_entry.get()
        try:
            new_amount = int(new_amount_str)
            self.update_checked_out_books(username, new_amount)
        except ValueError:
            self.update_error_label.config(text="New Book Amount must be an integer", fg="red")

    def delete_user_wrapper(self):
        # Wrapper function to get entry values and call delete_user
        username = self.username_entry.get()
        self.delete_user(username)

    def create_user_wrapper(self):
        self.create_user()


if __name__ == "__main__":
    app = CRUD()
    app.open_create_user_window()
    tk.mainloop()
