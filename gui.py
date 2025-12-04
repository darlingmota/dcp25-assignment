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
