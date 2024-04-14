from bson.code import Code
from pymongo import MongoClient
import tkinter as tk

class MapReduce:
    def __init__(self, master):
        self.master = master
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['library_management']
        self.collection = self.db['library_collection']
        self.result_text = tk.Text(self.master, height=20, width=50)
        self.result_text.pack()

        update_button = tk.Button(self.master, text="Checked Out Books Per City",
                                  command=self.calculate_checked_out_books_by_city)
        update_button.pack()

    def calculate_checked_out_books_by_city(self):
        map_function = Code("""
            function() {
                emit(this.user_city, this.user_checked_out_books);
            }
        """)

        reduce_function = Code("""
            function(key, values) {
                return Array.sum(values);
            }
        """)

        result = self.db.command({
            "mapReduce": "library_collection",
            "map": map_function,
            "reduce": reduce_function,
            "out": {"inline": 1}
        })

        result_text_content = ""
        for doc in result["results"]:
            result_text_content += str(doc) + "\n"

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text_content)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Library Management System")

    map_reduce_gui = MapReduce(root)

    root.mainloop()
