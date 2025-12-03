import os 
import sqlite3
import pandas as pd

def get_connection(db_path: str = "tunes.db") -> sqlite3.Connection:
    return sqlite3.connect(db_path)

def create_table(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    