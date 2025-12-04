import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def get_connection(db_path="tunes.db"):
    return sqlite3.connect(db_path)


def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
        create table if not exists tunes (
            id integer primary key autoincrement,
            book_number integer,
            file_name text,
            ref_number text,
            title text,
            tune_type text,
            meter text,
            key text,
            abc_text text
        )
    """)
    conn.commit()

def clear_table(conn):
    cur = conn.cursor()
    cur.execute("delete from tunes")
    conn.commit()

def find_abc_files(root="abc_books"):
    files = []
    for path, folders, filelist in os.walk(root):
        folder_name = os.path.basename(path)
        if folder_name.isdigit():
            book_number = int(folder_name)
            for f in filelist:
                if f.endswith(".abc"):
                    full_path = os.path.join(path, f)
                    files.append({
                        "book": book_number,
                        "path": full_path,
                        "file_name": f
                    })
    return files

def parse_abc_file(path, book_number, file_name):
    tunes = []
    current = None
    body_lines = []
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            
            if text.startswith("X:"):
                
                if current:
                    current["abc_text"] = "\n".join(body_lines)
                    tunes.append(current)

                
                current = {
                    "book_number": book_number,
                    "file_name": file_name,
                    "ref_number": text[2:].strip(),
                    "title": "",
                    "tune_type": "",
                    "meter": "",
                    "key": "",
                    "abc_text": ""
                }
                body_lines = []
            elif current:
                if text.startswith("T:"):
                    current["title"] = text[2:].strip()
                elif text.startswith("R:"):
                    current["tune_type"] = text[2:].strip()
                elif text.startswith("M:"):
                    current["meter"] = text[2:].strip()
                elif text.startswith("K:"):
                    current["key"] = text[2:].strip()
                else:
                    body_lines.append(line.rstrip("\n"))

    if current:
        current["abc_text"] = "\n".join(body_lines)
        tunes.append(current)
    return tunes

def insert_tune(conn, tune):
    cur = conn.cursor()
    cur.execute("""
        insert into tunes (book_number, file_name, ref_number, title,
                           tune_type, meter, key, abc_text)
        values (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tune["book_number"],
        tune["file_name"],
        tune["ref_number"],
        tune["title"],
        tune["tune_type"],
        tune["meter"],
        tune["key"],
        tune["abc_text"]
    ))
    conn.commit()

def load_all_tunes(conn):
    clear_table(conn)
    abc_files = find_abc_files()
    total = 0
    for item in abc_files:
        tunes = parse_abc_file(item["path"], item["book"], item["file_name"])
        for t in tunes:
            insert_tune(conn, t)
        total += len(tunes)
    print("loaded", total, "tunes into the database")

def load_dataframe(conn):
    df = pd.read_sql("select * from tunes", conn)
    return df

def get_tunes_by_book(df, book_number):
    return df[df["book_number"] == book_number]

def get_tunes_by_type(df, tune_type):
    return df[df["tune_type"].str.lower() == tune_type.lower()]

def search_tunes(df, term):
    return df[df["title"].str.contains(term, case=False, na=False)]


def count_tunes_per_book(df):
    """Return number of tunes in each book."""
    return df.groupby("book_number")["id"].count()

def most_common_tune_types(df, n=10):
    """Return the most frequent tune types."""
    return df["tune_type"].value_counts().head(n)

def most_common_keys(df):
    """Return frequency of key signatures."""
    return df["key"].value_counts()

def average_tune_length(df):
    """Estimate tune length by counting bar symbols in abc_text."""
    return df["abc_text"].apply(lambda x: x.count("|")).mean()

def tunes_by_meter(df):
    """Return counts for each meter."""
    return df["meter"].value_counts()

def tunes_per_file(df):
    """Return number of tunes contained in each ABC file."""
    return df.groupby("file_name")["id"].count()
def plot_tunes_per_book(df):
    """Display a bar chart showing number of tunes per book."""
    counts = df.groupby("book_number")["id"].count()
    plt.figure(figsize=(8,5))
    counts.plot(kind="bar", color="#4A90E2")
    plt.title("Number of Tunes per Book")
    plt.xlabel("Book Number")
    plt.ylabel("Tune Count")
    plt.tight_layout()
    plt.show()

def plot_most_common_keys(df, n=10):
    """Display a bar chart showing the most common key signatures."""
    counts = df["key"].value_counts().head(n)
    plt.figure(figsize=(8,5))
    counts.plot(kind="bar", color="#7E57C2")
    plt.title("Most Common Key Signatures")
    plt.xlabel("Key")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

def main():
    conn = get_connection()
    create_table(conn)

    print("loading tunes...")
    load_all_tunes(conn)

    df = load_dataframe(conn)

    while True:
        print()
        print("=== abc tunes explorer ===")
        print("1) show number of tunes loaded")
        print("2) list tunes by book")
        print("3) list tunes by type")
        print("4) search tunes by title")
        print("5) show first 5 rows")
        print("6) count tunes per book")
        print("7) most common tune types")
        print("8) most common key signatures")
        print("9) plot tunes per book")
        print("10) plot most common keys")
        print("0) quit")
        print()

        choice = input("enter choice: ")

        if choice == "1":
            print("total tunes:", len(df))

        elif choice == "2":
            book = int(input("book number: "))
            result = get_tunes_by_book(df, book)
            print(result)

        elif choice == "3":
            t = input("tune type: ")
            result = get_tunes_by_type(df, t)
            print(result)

        elif choice == "4":
            term = input("search term: ")
            result = search_tunes(df, term)
            print(result)

        elif choice == "5":
            print(df.head())

        elif choice == "6":
            print(count_tunes_per_book(df))

        elif choice == "7":
            print(most_common_tune_types(df))

        elif choice == "8":
            print(most_common_keys(df))

        elif choice == "9":
            plot_tunes_per_book(df)

        elif choice == "10":
            plot_most_common_keys(df)

        elif choice == "0":
            print("goodbye")
            break

        else:
            print("invalid choice")

if __name__ == "__main__":
    main()
