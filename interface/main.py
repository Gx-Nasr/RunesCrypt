import tkinter as tk
import json
from pathlib import Path

root = tk.Tk()
root.title("Gx-Encrypter")
root.geometry("720x720")

file_name = "user.json"


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def login_screen():
    clear_window()

    title = tk.Label(root, text="Login", font=("Arial", 24))
    title.pack(pady=100)

    username_entry = tk.Entry(root, font=("Arial", 16))
    username_entry.pack(pady=10)

    password_entry = tk.Entry(root, font=("Arial", 16), show="*")
    password_entry.pack(pady=10)

    login_button = tk.Button(
        root,
        text="Login",
        font=("Arial", 16),
        bg="green",
        fg="white",
        command=root.destroy
    )
    login_button.pack(pady=20)

    username_entry.bind(
        "<Return>",
        lambda event: password_entry.focus()
    )

    password_entry.bind(
        "<Return>",
        lambda event: login_button.invoke()
    )


def json_dump(user, password):
    tmp_json = {
        "login": user,
        "password": password
    }
    try:
        with open("user.json", "w") as json_file:
            json.dump(tmp_json, json_file, indent=2)
    except BaseException:
        pass
    

def create_screen():
    clear_window()

    title = tk.Label(root, text="Create Account", font=("Arial", 24))
    title.pack(pady=20)

    username_entry = tk.Entry(root, font=("Arial", 16))
    username_entry.pack(pady=10)

    password_entry = tk.Entry(root, font=("Arial", 16), show="*")
    password_entry.pack(pady=10)

    def create_account():
        json_dump(username_entry.get(), password_entry.get())
        root.destroy()

    create_button = tk.Button(
        root,
        text="Create",
        font=("Arial", 16),
        bg="green",
        fg="white",
        command=create_account
    )
    create_button.pack(pady=20)

    username_entry.bind(
        "<Return>",
        lambda event: password_entry.focus()
    )

    password_entry.bind(
        "<Return>",
        lambda event: create_account()
    )



if Path(file_name).exists():
    button = tk.Button(
        root,
        text="Login",
        bg="blue",
        fg="white",
        font=("Arial", 16),
        width=10,
        height=2,
        command=login_screen
    )
    button.bind("<Return>", lambda event: login_screen())
    button.focus()

else:
    button = tk.Button(
        root,
        text="Create Acc",
        bg="blue",
        fg="white",
        font=("Arial", 16),
        width=10,
        height=2,
        command=create_screen
    )
    button.bind("<Return>", lambda event: create_screen())
    button.focus


button.pack(pady=300)

root.mainloop()