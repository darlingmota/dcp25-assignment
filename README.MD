# Music Analysis, GUI Application & Database Processing Project 2025


- Name: Darling Mota

- Student Number: C24486262

- Module: Data Centric Programming

**Lecturered by** *Dr. Bryan Duggan, Computer Scientist*

# Screenshots
![GUI Screenshot](images/Screenshot%202025-12-04%20at%2013.53.07.png)
![Chart Screenshot](images/Screenshot%202025-12-04%20at%2017.04.46.png)



# List of files in the project

| File / Folder | Source / Description |
|---------------|----------------------|
| full_program.py | Self written backend |
| gui.py | Self written |
| assignment.md | Assignment brief |
| abc_books/ | Files provided in assignment |
| images/headerImage.png | GUI header image |
| tunes.db | SQLite database |
| README.md | Project documentation |
| .gitignore | Ignore |
| LICENSE | Permissions by Darling Mota (c)|

# Description of the project

For those reading, I created a parser that reads multiple folders of ABC files which in turn identifies each tune inside them and uses that information to insert every tune into a database for analysis.

# Instructions for use

Make sure to use the full_program.py file which opens the command line interface and from there you can understand the data analysis. Along with using gui.py file it will open a pretty nice menu based interface and from there you can manually use the search options. Both connect to the same database and analysis functions.

# How it works:
## Parser:
- I scan the entrie abc_books folder and look inside each numbered subfolder which are 1 and 2.
- Every .abc file is read line by line to identify tune selections by markers like X: T: R: K: those are handy!
- I store each tunes as a dictionary containing all of its metadata and its body text
- The parser supports files that hold a lot tunes in one file

## Database:
- I create a SQLite database called tunes.db the first time the program runs.
- I create a tunes table with columns such as the book number, the reference number, title, tune type, meter, key, and the full ABC text.
- Every tune gotten or extracted by the parser gets inserted into the database with the correct folder
- The database acts as the main storage system for all searches and analysis

## Pandas Data Analysis:
- I loaded the entire database into a pandaas DataFrame for analysis.
- I analyse tune frequencies, such as how many tunes are in each book.
- I calculate the most common tune types and key signatures.
- I generate charts using matplotllib to visualise these statistics.

## Tkinter:
- Built a user interface with a TU Dublin header image aimed at students
- The GUI allows the users to search by book number, tune type or tune title
- Results appear in a scrollable table with labelled columns
- The GUI includes buttons that trigger matplotlib charts such as "Tunes Per Book" and "Most Common Keys"
![Chart Screenshot](images/Screenshot%202025-12-04%20at%2017.04.46.png)
![Chart2 Screenshot](images/Screenshot%202025-12-04%20at%2017.41.42.png)
- The GUI uses the backend functions meaning both interfaces stays consistent

## Command Line Interface Menu:
- I also included a command line interface that lets the users use the functions easily
- The menu can show tune counts, search results, DataFrame samples and analysis outputs
- I included extra options for generating plots directly through the CLI

## GUI Header:
- Adding a TU Dublin header image to give the GUI a branded look
- The image is resized using PIL to fit the top of the window 
- The image makes the GUI feel more complete and professional


# What I am most proud of in the assignment

I like the GUI I created.
![GUI Screenshot](images/Screenshot%202025-12-04%20at%2013.53.07.png)
 It's overall just user friendly and sleek and works perfectly with the databaase and analysis features underneath. Adding the analysis charts into the GUI really made the project feel more complete and gives the user a sense of variety and understand some facts

# What I learned

This assignment taiught me how to parse real world text formats and work with massive amounts of data. I learned a lot on how to work with SQLite databases and how to use pandas for analysing structed data. Learned some things about the structuring of visualisations with matplotlib and how to design a GUI that interacts with a backend system. Really, it helped me understand how different parts of a data centric application fit together from file processing all the way to user interaction.


# References
* **Duggan, B. (2025)** *Tkinter GUI Programming: A Comprehensive Guide to Python's built-in GUI Library. TU Dublin*
* 
* 
* 
* 
* 


