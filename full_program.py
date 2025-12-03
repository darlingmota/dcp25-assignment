import os
import sqlite3
import pandas as pd

def get_connection(db_path: str = "tunes.db") -> sqlite3.Connection: