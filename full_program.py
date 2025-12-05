import os  # imports operating system functions for walking directories
import sqlite3  # imports sqlite library for database operations
import pandas as pd  # imports pandas for dataframe based analysis
import matplotlib.pyplot as plt  # imports matplotlib for plotting graphs/charts 

def get_connection(db_path="tunes.db"):  # defines function to get database connection
    return sqlite3.connect(db_path)  # opens a connection to the sqlite database

def create_table(conn):
    cur = conn.cursor()  # creates cursor for executing sql

    # creates the tunes table if it does not exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tunes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_number INTEGER,
            file_name TEXT,
            ref_number INTEGER,
            title TEXT,
            tune_type TEXT,
            meter TEXT,
            key TEXT
        );
    """)  # ends sql command

    conn.commit()  # saves changes

def clear_table(conn):  # defines function to clear all tunes from the table
    cur = conn.cursor()  # creates cursor
    cur.execute("delete from tunes")  # removes all rows from tunes table
    conn.commit()  # saves deletion

def find_abc_files(root="abc_books"):  # defines function to find all abc files in directory tree
    files = []  # list to store files found
    for path, folders, filelist in os.walk(root):  # walks directories recursively
        folder_name = os.path.basename(path)  # gets the folder name as a string
        if folder_name.isdigit():  # checks if folder name is a book number
            book_number = int(folder_name)  # converts folder name to integer
            for f in filelist:  # loops through all files in the folder
                if f.endswith(".abc"):  # checks if file is an abc file
                    full_path = os.path.join(path, f)  # constructs full file path
                    files.append({  # stores file metadata
                        "book": book_number,
                        "path": full_path,
                        "file_name": f
                    })
    return files  # returns list of abc file info

def parse_abc_file(path, book_number, file_name):  # defines function to parse abc file into tunes
    tunes = []  # stores parsed tunes
    current = None  # holds current tune being parsed
    body_lines = []  # stores abc body lines
    
    with open(path, "r", encoding="utf-8") as f:  # opens abc file for reading
        for line in f:  # loops through each line
            text = line.strip()  # removes whitespace
            
            if text.startswith("X:"):  # detects new tune start
                
                if current:  # if a tune was already being read
                    current["abc_text"] = "\n".join(body_lines)  # save tune body
                    tunes.append(current)  # store completed tune

                
                current = {  # creates new tune dictionary
                    "book_number": book_number,
                    "file_name": file_name,
                    "ref_number": text[2:].strip(),
                    "title": "",
                    "tune_type": "",
                    "meter": "",
                    "key": "",
                    "abc_text": ""
                }
                body_lines = []  # reset body buffer
            elif current:  # if currently parsing a tune
                if text.startswith("T:"):  # tune title
                    current["title"] = text[2:].strip()  # extract title
                elif text.startswith("R:"):  # tune type
                    current["tune_type"] = text[2:].strip()  # extract tune type
                elif text.startswith("M:"):  # meter
                    current["meter"] = text[2:].strip()  # extract meter
                elif text.startswith("K:"):  # key signature
                    current["key"] = text[2:].strip()  # extract key
                else:
                    body_lines.append(line.rstrip("\n"))  # add line to tune body

    if current:  # if last tune not yet appended
        current["abc_text"] = "\n".join(body_lines)  # save last tune body
        tunes.append(current)  # append last tune
    return tunes  # return list of parsed tunes

def insert_tune(conn, tune):  # defines function to insert a tune into database
    cur = conn.cursor()  # creates cursor
    cur.execute("""
        insert into tunes (book_number, file_name, ref_number, title,
                           tune_type, meter, key, abc_text)
        values (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tune["book_number"],  # book number
        tune["file_name"],  # file name
        tune["ref_number"],  # reference number
        tune["title"],  # tune title
        tune["tune_type"],  # tune type
        tune["meter"],  # meter
        tune["key"],  # key signature
        tune["abc_text"]  # abc notation text
    ))
    conn.commit()  # save changes to database

def load_all_tunes(conn):  # defines function to load all tunes from abc files into database
    clear_table(conn)  # clears existing tunes from database
    abc_files = find_abc_files()  # finds all abc files
    total = 0  # initialize tune count
    for item in abc_files:  # iterate over abc files
        tunes = parse_abc_file(item["path"], item["book"], item["file_name"])  # parse tunes from file
        for t in tunes:  # iterate tunes
            insert_tune(conn, t)  # insert each tune into database
        total += len(tunes)  # update total count
    print("loaded", total, "tunes into the database")  # print summary

def load_dataframe(conn):  # defines function to load tunes table into pandas dataframe
    df = pd.read_sql("select * from tunes", conn)  # read entire tunes table into dataframe
    return df  # return dataframe

def get_tunes_by_book(df, book_number):  # defines function to filter tunes by book number
    return df[df["book_number"] == book_number]  # filter dataframe by book_number

def get_tunes_by_type(df, tune_type):  # defines function to filter tunes by tune type
    return df[df["tune_type"].str.lower() == tune_type.lower()]  # case insensitive filter by tune_type

def search_tunes(df, term):  # defines function to search tunes by title substring
    return df[df["title"].str.contains(term, case=False, na=False)]  # case insensitive substring search

def count_tunes_per_book(df):  # defines function to count tunes per book
    """Return number of tunes in each book."""
    return df.groupby("book_number")["id"].count()  # group by book_number and count tunes

def most_common_tune_types(df, n=10):  # defines function to get most common tune types
    """Return the most frequent tune types."""
    return df["tune_type"].value_counts().head(n)  # count tune_type frequencies and take top n

def most_common_keys(df):  # defines function to get frequency of key signatures
    """Return frequency of key signatures."""
    return df["key"].value_counts()  # count key signature frequencies

def average_tune_length(df):  # defines function to estimate average tune length
    """Estimate tune length by counting bar symbols in abc_text."""
    return df["abc_text"].apply(lambda x: x.count("|")).mean()  # count bars '|' and average

def tunes_by_meter(df):  # defines function to count tunes by meter
    """Return counts for each meter."""
    return df["meter"].value_counts()  # count meter frequencies

def tunes_per_file(df):  # defines function to count tunes per abc file
    """Return number of tunes contained in each ABC file."""
    return df.groupby("file_name")["id"].count()  # group by file_name and count tunes


def plot_tunes_per_book(df):  # defines function to plot tunes per book as bar chart
    """Display a bar chart showing number of tunes per book."""
    counts = df.groupby("book_number")["id"].count()  # count tunes per book
    plt.figure(figsize=(8,5))  # create figure with size
    counts.plot(kind="bar", color="#4A90E2")  # plot bar chart with color
    plt.title("Number of Tunes per Book")  # set plot title
    plt.xlabel("Book Number")  # set x-axis label
    plt.ylabel("Tune Count")  # set y-axis label
    plt.tight_layout()  # adjust layout
    plt.show()  # display plot

def plot_most_common_keys(df, n=10):  # defines function to plot most common keys
    """Display a bar chart showing the most common key signatures."""
    counts = df["key"].value_counts().head(n)  # get top n key counts
    plt.figure(figsize=(8,5))  # create figure
    counts.plot(kind="bar", color="#7E57C2")  # plot bar chart with color
    plt.title("Most Common Key Signatures")  # set title
    plt.xlabel("Key")  # set x-axis label
    plt.ylabel("Frequency")  # set y-axis label
    plt.tight_layout()  # adjust layout
    plt.show()  # show plot

def main():  # defines main function for interactive menu
    conn = get_connection()  # connect to database
    create_table(conn)  # create tunes table if needed

    print("loading tunes...")  # notify loading start
    load_all_tunes(conn)  # load tunes into database

    df = load_dataframe(conn)  # load tunes into dataframe

    while True:  # infinite loop for menu
        print()  # blank line
        print("=== abc tunes explorer ===")  # menu header
        print("1) show number of tunes loaded")  # option 1
        print("2) list tunes by book")  # option 2
        print("3) list tunes by type")  # option 3
        print("4) search tunes by title")  # option 4
        print("5) show first 5 rows")  # option 5
        print("6) count tunes per book")  # option 6
        print("7) most common tune types")  # option 7
        print("8) most common key signatures")  # option 8
        print("9) plot tunes per book")  # option 9
        print("10) plot most common keys")  # option 10
        print("0) quit")  # option 0
        print()  # blank line

        choice = input("enter choice: ")  # get user input

        if choice == "1":  # if user selects 1
            print("total tunes:", len(df))  # print total number of tunes

        elif choice == "2":  # if user selects 2
            book = int(input("book number: "))  # prompt for book number
            result = get_tunes_by_book(df, book)  # filter tunes by book
            print(result)  # print results

        elif choice == "3":  # if user selects 3
            t = input("tune type: ")  # prompt for tune type
            result = get_tunes_by_type(df, t)  # filter tunes by type
            print(result)  # print results

        elif choice == "4":  # if user selects 4
            term = input("search term: ")  # prompt for search term
            result = search_tunes(df, term)  # search tunes by title
            print(result)  # print results

        elif choice == "5":  # if user selects 5
            print(df.head())  # print first 5 rows of dataframe

        elif choice == "6":  # if user selects 6
            print(count_tunes_per_book(df))  # print count of tunes per book

        elif choice == "7":  # if user selects 7
            print(most_common_tune_types(df))  # print most common tune types

        elif choice == "8":  # if user selects 8
            print(most_common_keys(df))  # print most common keys

        elif choice == "9":  # if user selects 9
            plot_tunes_per_book(df)  # plot tunes per book

        elif choice == "10":  # if user selects 10
            plot_most_common_keys(df)  # plot most common keys

        elif choice == "0":  # if user selects 0
            print("goodbye")  # print goodbye message
            break  # exit loop

        else:  # if invalid choice
            print("invalid choice")  # notify invalid input

if __name__ == "__main__":  # if script is run directly
    main()  # call main function
