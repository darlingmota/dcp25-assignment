import os
import sqlite3
import pandas as pd

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
def main():
    conn = get_connection()
    create_table(conn)

    abc_files = find_abc_files()
    print("found", len(abc_files), "abc files")

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
if __name__ == "__main__":
    main()
