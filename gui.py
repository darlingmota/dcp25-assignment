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
