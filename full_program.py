import os
import sqlite3
import pandas as pd

def get_connection(db_path="tunes.db"):
    conn = sqlite3.connect(db_path)
    return conn


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

def main():
    conn = get_connection()
    create_table(conn)
    print("database ready")

if __name__ == "__main__":
    main()