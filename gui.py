import tkinter as tk  # imports tkinter for gui creation
from tkinter import ttk  # imports themed tkinter widgets
from PIL import Image, ImageTk  # imports pillow for image handling
from full_program import(  # imports backend logic from full_program
    get_connection, create_table, load_all_tunes,
    load_dataframe, get_tunes_by_book,
    get_tunes_by_type, search_tunes,
    plot_tunes_per_book, plot_most_common_keys
)  # imports functions used by gui

conn = get_connection()  # opens database connection
create_table(conn)  # ensures tunes table exists
load_all_tunes(conn)  # loads tunes from abc files into database
df = load_dataframe(conn)  # loads tunes table into pandas dataframe

root = tk.Tk()  # creates root window
root.title("ABC Tunes Explorer")  # sets window title
root.geometry("1050x800")  # sets window size
root.configure(bg="#121212")  # sets background color

logo_img = Image.open("images/headerImage.png")  # loads header image
logo_img = logo_img.resize((300, 180))  # resizes image
logo_img = ImageTk.PhotoImage(logo_img)  # converts image for tkinter
logo_label = tk.Label(root, image=logo_img, bg="#121212")  # creates image label
logo_label.pack(pady=10)  # packs logo with padding

ACCENT = "white"  # accent color
BG = "#121212"  # background color
PANEL = "#1C1C1C"  # sidebar panel color
TEXT = "#EAEAEA"  # general text color
FONT = ("Inter", 11)  # default font
FONT_BOLD = ("Inter", 12, "bold")  # bold font
TITLE_FONT = ("Inter", 22, "bold")  # title font

def modern_button(parent, text, command):  # function to create styled buttons
    style = ttk.Style()  # creates ttk style manager
    style.theme_use("clam")  # uses clam theme
    style.configure(  # configures dark button style
        "Dark.TButton",
        background="#000000",
        foreground="white",
        borderwidth=0,
        focusthickness=0,
        focuscolor=parent["bg"],
        padding=6
    )  # sets button appearance
    style.map(
        "Dark.TButton",
        background=[("active", "#000000")],
        foreground=[("active", "white")]
    )  # sets hover behavior
    return ttk.Button(  # returns styled button
        parent,
        text=text,
        command=command,
        style="Dark.TButton"
    )

header = tk.Label(  # creates main title label
    root,
    text="ABC Tunes Explorer",
    font=TITLE_FONT, fg="white",
    bg=BG,
)
header.pack(pady=15)  # packs header with spacing



subtitle = tk.Label(  # creates subtitle label
    root,
    text="Your way for finding Irish ABC Tunes",
    font=("Inter", 12),
    fg="white",
    bg=BG,
)
subtitle.pack(pady=0)  # packs subtitle

sidebar = tk.Frame(root, bg=PANEL, width=260)  # creates left sidebar frame
sidebar.pack(side="left", fill="y")  # packs sidebar vertically

tk.Label(  # section title label
    sidebar,
    text="Search Options",
    bg=PANEL, fg="white",
    font=("Inter", 14, "bold")
).pack(pady=15)  # packs label

def field(label):  # helper function to create labeled entry field
    tk.Label(sidebar, text=label, bg=PANEL, fg=TEXT, font=FONT).pack(anchor="w", padx=20)  # creates label
    entry = tk.Entry(sidebar, font=FONT, bg="#1A1A1A", fg="white", relief="flat", insertbackground="white", highlightthickness=2, highlightbackground="#333333", highlightcolor="#555555")  # creates entry box
    entry.pack(fill="x", padx=20, pady=5)  # packs entry
    return entry  # returns entry

book_entry = field("Book Number")  # entry for book search
type_entry = field("Tune Type")  # entry for type search
search_entry = field("Title Contains")  # entry for title search

def do_book():  # handles book search
    try:
        num = int(book_entry.get())  # gets book number
        update_table(get_tunes_by_book(df, num))  # updates table with results
    except:
        update_table(df)  # fallback show all tunes



def do_type():  # handles type search
    update_table(get_tunes_by_type(df, type_entry.get()))  # updates table with type results

def do_title():  # handles title partial search
    update_table(search_tunes(df, search_entry.get()))  # updates table with title search results




def do_reload():  # reloads database
    load_all_tunes(conn)  # reload tunes
    global df  # updates dataframe globally
    df = load_dataframe(conn)  # refresh dataframe
    update_table(df)  # refresh table

modern_button(sidebar, "Search by Book", do_book).pack(fill="x", padx=20, pady=12)  # adds book button

modern_button(sidebar, "Search by Type", do_type).pack(fill="x", padx=20, pady=12)  # adds type button

modern_button(sidebar, "Search by Title", do_title).pack(fill="x", padx=20, pady=12)  # adds title button

tk.Label(sidebar, bg=PANEL).pack(pady=10)  # spacing label
modern_button(sidebar, "Reload Database", do_reload).pack(fill="x", padx=20, pady=12)  # reload button

tk.Label(sidebar, text="Analysis", bg=PANEL, fg="white",         font=("Inter", 14, "bold")).pack(pady=10)  # analysis section title

def do_plot_books():  # use def to bar chart for tunes per book
    plot_tunes_per_book(df)  # plots tunes per book

def do_plot_keys():  # use def to call chart for common keys
    plot_most_common_keys(df)  # plots most common keys

modern_button(sidebar, "Plot Tunes Per Book", do_plot_books).pack(fill="x", padx=20, pady=12)  # plot button
modern_button(sidebar, "Plot Most Common Keys", do_plot_keys).pack(fill="x", padx=20, pady=12)  # plot button

table_frame = tk.Frame(root, bg=BG)  # creates area for results table
table_frame.pack(side="right", expand=True, fill="both")  # packs table frame

columns = ("id", "book", "file", "ref", "title", "type", "meter", "key")  # table columns
result_box = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)  # creates treeview table

style = ttk.Style()  # style manager
style.theme_use("clam")  # uses clam theme
style.configure(  # styles treeview rows
    "Treeview",
    background="#1C1C1C",
    foreground="white",
    rowheight=32,
    fieldbackground="#1C1C1C",
    bordercolor="#1C1C1C",
    borderwidth=0,
    highlightthickness=0
)  # configures treeview background and appearance
style.configure(  # styles table headings
    "Treeview.Heading",
    font=("Inter", 11, "bold"),
    background="#1C1C1C",
    foreground="white",
    relief="flat",
    borderwidth=0
)  # configures heading appearance
style.map(  # defines selection behavior
    "Treeview",
    background=[("selected", "#333333")],
    foreground=[("selected", "white")],
    relief=[("selected", "flat")]
)  # sets selected row colors and relief

for col in columns:  # configures each column
    result_box.heading(col, text=col.upper())  # sets heading text
    result_box.column(col, width=120)  # sets column width

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=result_box.yview)  # made a vertical scrollbar
result_box.configure(yscrollcommand=scrollbar.set)  # links scroll to table

scrollbar.pack(side="right", fill="y")  # packs scrollbar
result_box.pack(side="left", expand=True, fill="both")  # packs table

def update_table(dataframe):  # function to refresh table
    result_box.delete(*result_box.get_children())  # clears table
    
    for _, row in dataframe.iterrows():  # loops through dataframe rows
        result_box.insert("", "end", values=(  # inserts row
            row["id"],
            row["book_number"],
            row["file_name"],
            row["ref_number"],
            row["title"],
            row["tune_type"],
            row["meter"],
            row["key"]
        ))  # inserts row values

update_table(df)  # fills table with the data

root.logo_img = logo_img  # prevents image garbage collection
root.mainloop()  # starts gui loop