def create_user(self, user_name, checked_out_books, city, book_name):
    new_user = {
        "user_name": user_name,
        "user_checked_out_books": checked_out_books,
        "user_city": city,
        "book_name": book_name
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