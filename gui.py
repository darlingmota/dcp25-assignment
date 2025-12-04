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

header = tk.Label(
    root,
    text="ABC Tunes Explorer",
    font=TITLE_FONT, fg="white",
    bg=BG,
)
header.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Your way for finding Irish ABC Tunes",
    font=("Inter", 12),
    fg="white",
    bg=BG,
)
subtitle.pack(pady=0)

sidebar = tk.Frame(root, bg=PANEL, width=260, height=700)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="Search Options",
    bg=PANEL, fg="white",
    font=("Inter", 14, "bold")
).pack(pady=15)

def field(label):
    tk.Label(sidebar, text=label, bg=PANEL, fg=TEXT, font=FONT).pack(anchor="w", padx=20)
    entry = tk.Entry(sidebar, font=FONT, bg="#1A1A1A", fg="white", relief="flat", insertbackground="white", highlightthickness=2, highlightbackground="#333333", highlightcolor="#555555")
    entry.pack(fill="x", padx=20, pady=5)
    return entry

book_entry = field("Book Number")
type_entry = field("Tune Type")
search_entry = field("Title Contains")

def do_book():
    try:
        num = int(book_entry.get())
        update_table(get_tunes_by_book(df, num))
    except:
        update_table(df)

def do_type():
    update_table(get_tunes_by_type(df, type_entry.get()))

def do_title():
    update_table(search_tunes(df, search_entry.get()))

def do_reload():
    load_all_tunes(conn)
    global df
    df = load_dataframe(conn)
    update_table(df)

modern_button(sidebar, "Search by Book", do_book).pack(fill="x", padx=20, pady=12)
modern_button(sidebar, "Search by Type", do_type).pack(fill="x", padx=20, pady=12)
modern_button(sidebar, "Search by Title", do_title).pack(fill="x", padx=20, pady=12)

tk.Label(sidebar, bg=PANEL).pack(pady=10) 
modern_button(sidebar, "Reload Database", do_reload).pack(fill="x", padx=20, pady=12)


table_frame = tk.Frame(root, bg=BG)
table_frame.pack(side="right", expand=True, fill="both")

columns = ("id", "book", "file", "ref", "title", "type", "meter", "key")
result_box = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background="#1C1C1C",
    foreground="white",
    rowheight=32,
    fieldbackground="#1C1C1C",
    bordercolor="#1C1C1C",
    borderwidth=0,
    highlightthickness=0
)
style.configure(
    "Treeview.Heading",
    font=("Inter", 11, "bold"),
    background="#1C1C1C",
    foreground="white",
    relief="flat",
    borderwidth=0
)
style.map(
    "Treeview",
    background=[("selected", "#333333")],
    foreground=[("selected", "white")],
    relief=[("selected", "flat")]
)


for col in columns:
    result_box.heading(col, text=col.upper())
    result_box.column(col, width=120)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=result_box.yview)
result_box.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
result_box.pack(side="left", expand=True, fill="both")


def update_table(dataframe):
    result_box.delete(*result_box.get_children())
    for _, row in dataframe.iterrows():
        result_box.insert("", "end", values=(
            row["id"],
            row["book_number"],
            row["file_name"],
            row["ref_number"],
            row["title"],
            row["tune_type"],
            row["meter"],
            row["key"]
        ))

update_table(df)

root.logo_img = logo_img
root.mainloop()