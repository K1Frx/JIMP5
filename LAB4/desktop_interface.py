import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from typing import List, Union
import requests
from dataclasses import dataclass

@dataclass
class Movie:
    id: int
    title: str
    description: str
    director: str
    category: str
    year: int
    created_at: str
    updated_at: str
    rating: float

@dataclass
class Category:
    id: int
    name: str

class MovieViewModel:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api/movies/"

    def get_movies(self, title=None, director=None, category=None, year=None) -> List[Movie]:
        params = {"title": title, "director": director, "category": category, "year": year}
        response = requests.get(self.base_url, params=params)
        movies_data = response.json()
        movies = [Movie(**movie) for movie in movies_data]
        return movies

    def create_movie(self, data):
        response = requests.post(self.base_url, json=data)
        return Movie(**response.json())

    def update_movie(self, movie_id, data):
        url = f"{self.base_url}{movie_id}/"
        response = requests.patch(url, json=data)
        return Movie(**response.json())

    def delete_movie(self, movie_id):
        url = f"{self.base_url}{movie_id}/"
        response = requests.delete(url)
        return response.status_code == 204

class CategoryViewModel:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api/categories/"

    def get_categories(self, name=None) -> List[Category]:
        params = {"name": name}
        response = requests.get(self.base_url, params=params)
        categories_data = response.json()
        categories = [Category(**category) for category in categories_data]
        return categories

    def create_category(self, data):
        response = requests.post(self.base_url, json=data)
        return Category(**response.json())

    def update_category(self, category_id, data):
        url = f"{self.base_url}{category_id}/"
        response = requests.patch(url, json=data)
        return Category(**response.json())

    def delete_category(self, category_id):
        url = f"{self.base_url}{category_id}/"
        response = requests.delete(url)
        return response.status_code == 204

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")

        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=20)

        self.movies_button = tk.Button(self.menu_frame, text="Movies", command=self.open_movies_view)
        self.movies_button.pack(side=tk.LEFT, padx=10)

        self.categories_button = tk.Button(self.menu_frame, text="Categories", command=self.open_categories_view)
        self.categories_button.pack(side=tk.LEFT, padx=10)

    def open_movies_view(self):
        self.root.destroy()
        root_movies = tk.Tk()
        movie_view_model = MovieViewModel()
        movie_view = MovieView(root_movies, movie_view_model)
        root_movies.mainloop()

    def open_categories_view(self):
        self.root.destroy()
        root_categories = tk.Tk()
        category_view_model = CategoryViewModel()
        category_view = CategoryView(root_categories, category_view_model)
        root_categories.mainloop()

class MovieView:
    def __init__(self, root, movie_view_model):
        self.root = root
        self.root.title("Movie Manager")

        self.movie_view_model = movie_view_model

        self.movies_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.movies_listbox.pack(pady=10)

        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh_movies)
        self.refresh_button.pack(pady=5)

        self.add_button = tk.Button(root, text="Add Movie", command=self.add_movie)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Movie", command=self.update_movie)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Movie", command=self.delete_movie)
        self.delete_button.pack(pady=5)
        
        self.show_details_button = tk.Button(root, text="Show Details", command=self.show_details)
        self.show_details_button.pack(pady=5)
        
        self.back_to_main_button = tk.Button(root, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_to_main_button.pack(pady=5)
        
        self.refresh_movies()

    def refresh_movies(self):
        self.movies_listbox.delete(0, tk.END)
        movies = self.movie_view_model.get_movies()
        for movie in movies:
            self.movies_listbox.insert(tk.END, movie.title)

    def add_movie(self):
        new_movie_data = self.get_movie_data_from_user()
        if new_movie_data:
            created_movie = self.movie_view_model.create_movie(new_movie_data)
            messagebox.showinfo("Info", f"New movie added: {created_movie.title}")
            self.refresh_movies()

    def update_movie(self):
        selected_index = self.movies_listbox.curselection()
        if selected_index:
            selected_movie_title = self.movies_listbox.get(selected_index)
            selected_movie = self.movie_view_model.get_movies(title=selected_movie_title)[0]

            updated_movie_data = self.get_movie_data_from_user(selected_movie)
            if updated_movie_data:
                updated_movie = self.movie_view_model.update_movie(selected_movie.id, updated_movie_data)
                messagebox.showinfo("Info", f"Movie updated: {updated_movie.title}")
                self.refresh_movies()
        else:
            messagebox.showwarning("Warning", "Select a movie to update!")

    def delete_movie(self):
        selected_index = self.movies_listbox.curselection()
        if selected_index:
            selected_movie_title = self.movies_listbox.get(selected_index)
            confirmed = messagebox.askokcancel("Confirmation", f"Do you really want to delete the movie: {selected_movie_title}?")
            if confirmed:
                selected_movie = self.movie_view_model.get_movies(title=selected_movie_title)[0]
                deleted = self.movie_view_model.delete_movie(selected_movie.id)
                if deleted:
                    messagebox.showinfo("Info", f"Movie deleted: {selected_movie_title}")
                    self.refresh_movies()
                else:
                    messagebox.showerror("Error", "Failed to delete movie.")
        else:
            messagebox.showwarning("Warning", "Select a movie to delete!")

    def get_movie_data_from_user(self, movie=None):
        dialog_title = "Add Movie" if movie is None else f"Update Movie: {movie.title}"
        new_movie_data = simpledialog.askstring(dialog_title, "Enter movie data (comma-separated):",
                                                initialvalue=self.format_movie_data(movie))
        if new_movie_data:
            new_movie_data_list = new_movie_data.split(",")
            return {
                "title": new_movie_data_list[0].strip(),
                "description": new_movie_data_list[1].strip(),
                "director": new_movie_data_list[2].strip(),
                "category": new_movie_data_list[3].strip(),
                "year": int(new_movie_data_list[4].strip()),
                "rating": float(new_movie_data_list[5].strip()) if len(new_movie_data_list) > 5 else None
            }
        return None

    def format_movie_data(self, movie=None):
        if movie:
            return f"{movie.title}, {movie.description}, {movie.director}, {movie.category}, {movie.year}, {movie.rating or ''}"
        return ""
            
    def show_details(self):
        selected_index = self.movies_listbox.curselection()
        if selected_index:
            selected_movie_title = self.movies_listbox.get(selected_index)
            selected_movie = self.movie_view_model.get_movies(title=selected_movie_title)[0]

            details_window = tk.Toplevel(self.root)
            details_window.title("Movie Details")

            details_label = tk.Label(details_window, text=f"Details for {selected_movie.title}")
            details_label.pack(pady=10)

            details_text = f"Title: {selected_movie.title}\n" \
                           f"Description: {selected_movie.description}\n" \
                           f"Director: {selected_movie.director}\n" \
                           f"Category: {selected_movie.category}\n" \
                           f"Year: {selected_movie.year}\n" \
                           f"Rating: {selected_movie.rating}\n"

            details_textbox = tk.Text(details_window, height=10, width=40)
            details_textbox.insert(tk.END, details_text)
            details_textbox.config(state=tk.DISABLED)
            details_textbox.pack(pady=10)

        else:
            messagebox.showwarning("Warning", "Select a movie to show details!")
            
    def back_to_main_menu(self):
        self.root.destroy()
        root_main = tk.Tk()
        main_app = MainApp(root_main)
        root_main.mainloop()


class CategoryView:
    def __init__(self, root, category_view_model):
        self.root = root
        self.root.title("Category Manager")

        self.category_view_model = category_view_model

        self.categories_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.categories_listbox.pack(pady=10)

        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh_categories)
        self.refresh_button.pack(pady=5)

        self.add_button = tk.Button(root, text="Add Category", command=self.add_category)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Category", command=self.update_category)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Category", command=self.delete_category)
        self.delete_button.pack(pady=5)
        
        self.back_to_main_button = tk.Button(root, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_to_main_button.pack(pady=5)

        self.refresh_categories()

    def refresh_categories(self):
        self.categories_listbox.delete(0, tk.END)
        categories = self.category_view_model.get_categories()
        for category in categories:
            self.categories_listbox.insert(tk.END, category.name)

    def add_category(self):
        new_category_name = simpledialog.askstring("Input", "Enter new category name:")
        if new_category_name:
            new_category_data = {"name": new_category_name}
            created_category = self.category_view_model.create_category(new_category_data)
            messagebox.showinfo("Info", f"New category added: {created_category.name}")
            self.refresh_categories()

    def update_category(self):
        selected_index = self.categories_listbox.curselection()
        if selected_index:
            selected_category_name = self.categories_listbox.get(selected_index)
            updated_category_name = simpledialog.askstring("Input", "Enter updated category name:", initialvalue=selected_category_name)
            if updated_category_name:
                updated_category_data = {"name": updated_category_name}
                selected_category = self.category_view_model.get_categories(name=selected_category_name)[0]
                updated_category = self.category_view_model.update_category(selected_category.id, updated_category_data)
                messagebox.showinfo("Info", f"Category updated: {updated_category.name}")
                self.refresh_categories()
        else:
            messagebox.showwarning("Warning", "Select a category to update!")

    def delete_category(self):
        selected_index = self.categories_listbox.curselection()
        if selected_index:
            selected_category_name = self.categories_listbox.get(selected_index)
            confirmed = messagebox.askokcancel("Confirmation", f"Do you really want to delete the category: {selected_category_name}?")
            if confirmed:
                selected_category = self.category_view_model.get_categories(name=selected_category_name)[0]
                deleted = self.category_view_model.delete_category(selected_category.id)
                if deleted:
                    messagebox.showinfo("Info", f"Category deleted: {selected_category_name}")
                    self.refresh_categories()
                else:
                    messagebox.showerror("Error", "Failed to delete category.")
        else:
            messagebox.showwarning("Warning", "Select a category to delete!")
            
    def back_to_main_menu(self):
        self.root.destroy()
        root_main = tk.Tk()
        main_app = MainApp(root_main)
        root_main.mainloop()


if __name__ == "__main__":
    root_main = tk.Tk()
    main_app = MainApp(root_main)
    root_main.mainloop()
