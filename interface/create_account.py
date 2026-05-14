import tkinter as tk
from .ui_utils import clear_window, root, show_error, json_dump, file_name
from validat_data.validator import validate_password, validate_login
from interface.login import login_screen
from hash_sha_256.sha_256 import sha_256


def create_screen():
    clear_window()

    frame = tk.Frame(root, bg="#1e1e2e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title = tk.Label(frame, text="Create Account", font=("Arial", 24), fg="white", bg="#1e1e2e")
    title.pack(pady=20)

    tk.Label(frame, text="Login", fg="white", bg="#1e1e2e").pack()
    username_entry = tk.Entry(frame, font=("Arial", 16))
    username_entry.pack(pady=10)

    tk.Label(frame, text="Password", fg="white", bg="#1e1e2e").pack()
    password_entry = tk.Entry(frame, font=("Arial", 16), show="*")
    password_entry.pack(pady=10)

    def create_account():
        login = username_entry.get()
        password = password_entry.get()

        error = validate_login(login)
        if error:
            show_error(error)
            return

        error = validate_password(password)
        if error:
            show_error(error)
            return

        login = sha_256(login)
        password = sha_256(password)

        json_dump(login, password)
        login_screen()

    create_button = tk.Button(
        frame,
        text="Create",
        font=("Arial", 16),
        bg="#4CAF50",
        fg="white",
        command=create_account
    )
    create_button.pack(pady=20)

    username_entry.bind("<Return>", lambda e: password_entry.focus())
    password_entry.bind("<Return>", lambda e: create_account())

    username_entry.focus()