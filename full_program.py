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