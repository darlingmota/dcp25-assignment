import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from full_program import(
    get_connection, create_table, load_all_tunes,
    load_dataframe, get_tunes_by_book,
    get_tunes_by_type, search_tunes
)

conn = get_connection()
create_table(conn)
load_all_tunes(conn)
df = load_dataframe(conn)


root = tk.Tk()
root.title("ABC Tunes Explorer")
root.geometry("1050x700")
root.configure(bg="#121212")

logo_img = Image.open("images/headerImage.png")
logo_img = logo_img.resize((300, 180))  
logo_img = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(root, image=logo_img, bg="#121212")
logo_label.pack(pady=10)


ACCENT = "white"
BG = "#121212"
PANEL = "#1C1C1C"
TEXT = "#EAEAEA"
FONT = ("Inter", 11)
FONT_BOLD = ("Inter", 12, "bold")
TITLE_FONT = ("Inter", 22, "bold")

def modern_button(parent, text, command):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Dark.TButton",
        background="#000000",
        foreground="white",
        borderwidth=0,
        focusthickness=0,
        focuscolor=parent["bg"],
        padding=6
    )
    style.map(
        "Dark.TButton",
        background=[("active", "#000000")],
        foreground=[("active", "white")]
    )
    return ttk.Button(
        parent,
        text=text,
        command=command,
        style="Dark.TButton"
    )
