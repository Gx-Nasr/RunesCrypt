import tkinter as tk
from pathlib import Path
import os
from .ui_utils import root, file_name
from .login import login_screen
from .create_account import create_screen

frame = tk.Frame(root, bg="#1e1e2e")
frame.place(relx=0.5, rely=0.5, anchor="center")

if Path(file_name).exists():
    os.chmod(file_name, 0o666)
    button = tk.Button(
        frame,
        text="Login",
        bg="blue",
        fg="white",
        font=("Arial", 16),
        width=10,
        height=2,
        command=login_screen
    )
else:
    button = tk.Button(
        frame,
        text="Create Acc",
        bg="blue",
        fg="white",
        font=("Arial", 16),
        width=10,
        height=2,
        command=create_screen
    )

button.pack()
button.bind("<Return>", lambda e: button.invoke())
button.focus()

root.mainloop()