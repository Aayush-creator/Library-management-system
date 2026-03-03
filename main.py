import tkinter as tk
from tkinter import messagebox
import json
import os

def load_data():
    """Load users and movies from JSON file."""
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {"users": {}, "movies": []}

def save_data(data):
    """Save users and movies to JSON file."""
    with open("data.json", "w") as f:
        json.dump(data, f)

def show_login():
    """Show the login window."""
    login_win = tk.Tk()
    login_win.title("CineVault - Login")
    login_win.geometry("400x300")
    login_win.configure(bg="#1a1a2e")
    login_win.resizable(False, False)

    tk.Label(login_win, text="🎬 CineVault",
             bg="#1a1a2e", fg="#e94560",
             font=("Arial", 24, "bold")).pack(pady=20)

    tk.Label(login_win, text="Username",
             bg="#1a1a2e", fg="white",
             font=("Arial", 11)).pack()
    username_entry = tk.Entry(login_win, width=30,
                              font=("Arial", 11))
    username_entry.pack(pady=5)

    tk.Label(login_win, text="Password",
             bg="#1a1a2e", fg="white",
             font=("Arial", 11)).pack()
    password_entry = tk.Entry(login_win, width=30,
                              font=("Arial", 11), show="*")
    password_entry.pack(pady=5)

    def login():
        """Check username and password."""
        username = username_entry.get()
        password = password_entry.get()

        # Check if fields are empty
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        # Check if credentials are correct
        data = load_data()
        if username in data["users"] and data["users"][username] == password:
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            login_win.destroy()
            show_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    tk.Button(login_win, text="Login",
              bg="#e94560", fg="white",
              font=("Arial", 11, "bold"),
              width=20, command=login).pack(pady=10)

    tk.Button(login_win, text="Don't have an account? Sign Up",
              bg="#1a1a2e", fg="#e94560",
              font=("Arial", 9),
              border=0, command=lambda: [login_win.destroy(), show_signup()]).pack()

    login_win.mainloop()


def show_signup():
    """Show the signup window."""
    signup_win = tk.Tk()
    signup_win.title("CineVault - Sign Up")
    signup_win.geometry("400x300")
    signup_win.configure(bg="#1a1a2e")
    signup_win.resizable(False, False)

    tk.Label(signup_win, text="🎬 Create Account",
             bg="#1a1a2e", fg="#e94560",
             font=("Arial", 20, "bold")).pack(pady=20)

    tk.Label(signup_win, text="Username",
             bg="#1a1a2e", fg="white",
             font=("Arial", 11)).pack()
    username_entry = tk.Entry(signup_win, width=30,
                              font=("Arial", 11))
    username_entry.pack(pady=5)

    tk.Label(signup_win, text="Password",
             bg="#1a1a2e", fg="white",
             font=("Arial", 11)).pack()
    password_entry = tk.Entry(signup_win, width=30,
                              font=("Arial", 11), show="*")
    password_entry.pack(pady=5)

    def signup():
        """Register a new user."""
        username = username_entry.get()
        password = password_entry.get()

        # Check if fields are empty
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        # Check if username already exists
        data = load_data()
        if username in data["users"]:
            messagebox.showerror("Error", "Username already exists!")
            return

        # Save new user
        data["users"][username] = password
        save_data(data)
        messagebox.showinfo("Success", "Account created! Please login.")
        signup_win.destroy()
        show_login()

    tk.Button(signup_win, text="Sign Up",
              bg="#e94560", fg="white",
              font=("Arial", 11, "bold"),
              width=20, command=signup).pack(pady=10)

    tk.Button(signup_win, text="Already have an account? Login",
              bg="#1a1a2e", fg="#e94560",
              font=("Arial", 9),
              border=0, command=lambda: [signup_win.destroy(), show_login()]).pack()

    signup_win.mainloop()


def show_dashboard(current_user):
    """Show the main dashboard after login."""
    dash_win = tk.Tk()
    dash_win.title("CineVault - Dashboard")
    dash_win.geometry("700x500")
    dash_win.configure(bg="#1a1a2e")

    # Top bar
    top = tk.Frame(dash_win, bg="#16213e", pady=10)
    top.pack(fill=tk.X)

    tk.Label(top, text="🎬 CineVault",
             bg="#16213e", fg="#e94560",
             font=("Arial", 18, "bold")).pack(side=tk.LEFT, padx=15)

    tk.Label(top, text=f"Welcome, {current_user}!",
             bg="#16213e", fg="white",
             font=("Arial", 11)).pack(side=tk.RIGHT, padx=15)

    # Search bar
    search_frame = tk.Frame(dash_win, bg="#1a1a2e", pady=10)
    search_frame.pack(fill=tk.X, padx=20)

    tk.Label(search_frame, text="Search:",
             bg="#1a1a2e", fg="white",
             font=("Arial", 11)).pack(side=tk.LEFT)

    search_entry = tk.Entry(search_frame, width=30,
                            font=("Arial", 11))
    search_entry.pack(side=tk.LEFT, padx=10)

    def search_movies():
        """Search movies by title or genre."""
        keyword = search_entry.get().lower()
        data = load_data()
        results = [m for m in data["movies"]
                  if keyword in m["title"].lower()
                  or keyword in m["genre"].lower()]
        refresh_list(results)

    tk.Button(search_frame, text="Search",
              bg="#e94560", fg="white",
              command=search_movies).pack(side=tk.LEFT)

    tk.Button(search_frame, text="Show All",
              bg="#0f3460", fg="white",
              command=lambda: refresh_list(load_data()["movies"])).pack(side=tk.LEFT, padx=5)

    # Movie list
    list_frame = tk.Frame(dash_win, bg="#1a1a2e")
    list_frame.pack(fill=tk.BOTH, expand=True, padx=20)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    movie_listbox = tk.Listbox(list_frame,
                               font=("Arial", 11),
                               bg="#16213e", fg="white",
                               selectbackground="#e94560",
                               height=15,
                               yscrollcommand=scrollbar.set)
    movie_listbox.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=movie_listbox.yview)

    def refresh_list(movies):
        """Refresh the movie listbox."""
        movie_listbox.delete(0, tk.END)
        if not movies:
            movie_listbox.insert(tk.END, "  No movies found.")
        for m in movies:
            movie_listbox.insert(tk.END,
                f"  🎬 {m['title']}  |  {m['genre']}  |  {m['year']}  |  ⭐ {m['rating']}")

    refresh_list(load_data()["movies"])

    # Bottom buttons
    btn_frame = tk.Frame(dash_win, bg="#1a1a2e", pady=10)
    btn_frame.pack()

    def open_add_movie():
        """Open the add movie window."""
        add_win = tk.Toplevel(dash_win)
        add_win.title("Add Movie")
        add_win.geometry("350x350")
        add_win.configure(bg="#1a1a2e")

        fields = {}
        for label in ["Title", "Genre", "Year", "Rating (0-10)"]:
            tk.Label(add_win, text=label,
                     bg="#1a1a2e", fg="white",
                     font=("Arial", 11)).pack(pady=3)
            entry = tk.Entry(add_win, width=25, font=("Arial", 11))
            entry.pack()
            fields[label] = entry

        def save_movie():
            """Save the new movie."""
            title = fields["Title"].get()
            genre = fields["Genre"].get()
            year = fields["Year"].get()
            rating = fields["Rating (0-10)"].get()

            # Validate fields
            if not title or not genre or not year or not rating:
                messagebox.showerror("Error", "Please fill in all fields!")
                return

            try:
                year = int(year)
                rating = float(rating)
                if rating < 0 or rating > 10:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error",
                    "Year must be a number and Rating must be 0-10!")
                return

            # Save movie
            data = load_data()
            data["movies"].append({
                "title": title,
                "genre": genre,
                "year": year,
                "rating": rating,
                "added_by": current_user
            })
            save_data(data)
            messagebox.showinfo("Success", "Movie added!")
            add_win.destroy()
            refresh_list(load_data()["movies"])

        tk.Button(add_win, text="Add Movie",
                  bg="#e94560", fg="white",
                  font=("Arial", 11, "bold"),
                  width=20, command=save_movie).pack(pady=15)

    def delete_movie():
        """Delete the selected movie."""
        selected = movie_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a movie to delete!")
            return
        data = load_data()
        data["movies"].pop(selected[0])
        save_data(data)
        refresh_list(data["movies"])
        messagebox.showinfo("Success", "Movie deleted!")

    tk.Button(btn_frame, text="➕ Add Movie",
              bg="#e94560", fg="white",
              font=("Arial", 11, "bold"),
              width=15, command=open_add_movie).pack(side=tk.LEFT, padx=10)

    tk.Button(btn_frame, text="🗑️ Delete Movie",
              bg="#0f3460", fg="white",
              font=("Arial", 11, "bold"),
              width=15, command=delete_movie).pack(side=tk.LEFT, padx=10)

    tk.Button(btn_frame, text="🚪 Logout",
              bg="#333", fg="white",
              font=("Arial", 11, "bold"),
              width=10,
              command=lambda: [dash_win.destroy(), show_login()]).pack(side=tk.LEFT, padx=10)

    dash_win.mainloop()

if __name__ == "__main__":
    show_login()