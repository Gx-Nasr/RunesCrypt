import tkinter as tk
import json
import os

root = tk.Tk()
root.title("Gx-Encrypter")
root.geometry("720x720")
root.configure(bg="#1e1e2e")

file_name = ".user.json"

def show_error(msg, mode="show"):
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_window.geometry("300x150")

    tk.Label(error_window, text=str(msg), fg="red", wraplength=250).pack(pady=30)

    def on_ok():
        error_window.destroy()
        if mode == "exit":
            root.destroy()

    ok_button = tk.Button(error_window, text="OK", command=on_ok)
    ok_button.pack()
    error_window.bind("<Return>", lambda e: on_ok())


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def json_dump(user, password):
    tmp_json = {"login": user, "password": password}
    try:
        with open(file_name, "w") as f:
            json.dump(tmp_json, f, indent=2)
        os.chmod("../.user.json", 0o444)
    except BaseException as e:
        show_error(e, mode="exit")  
