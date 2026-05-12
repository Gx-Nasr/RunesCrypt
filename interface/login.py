import tkinter as tk
from validat_data.validator import validat_password_login
from interface.ui_utils import show_error
from .ui_utils import clear_window, root

def login_screen():
    clear_window()

    frame = tk.Frame(root, bg="#1e1e2e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title = tk.Label(frame, text="Login", font=("Arial", 24), fg="white", bg="#1e1e2e")
    title.pack(pady=20)

    tk.Label(frame, text="Login", fg="white", bg="#1e1e2e").pack()
    username_entry = tk.Entry(frame, font=("Arial", 16))
    username_entry.pack(pady=10)

    tk.Label(frame, text="Password", fg="white", bg="#1e1e2e").pack()
    password_entry = tk.Entry(frame, font=("Arial", 16), show="*")
    password_entry.pack(pady=10)

    def checker():
        login = username_entry.get()
        password = password_entry.get()
        try:
            result = validat_password_login(login, password)
        except BaseException:
            result = "Somthing wrong try again!"
        if result:
            show_error(result)
        else:
            root.destroy()

    login_button = tk.Button(
        frame,
        text="Login",
        font=("Arial", 16),
        bg="#4CAF50",
        fg="white",
        command=checker
    )
    login_button.pack(pady=20)

    username_entry.bind("<Return>", lambda e: password_entry.focus())
    password_entry.bind("<Return>", lambda e: login_button.invoke())

