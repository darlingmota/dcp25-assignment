# Data Centric Programming Assignment 2025


Name: Darling Mota

Student Number: C24486262

Module: Data Centric Programming

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
| LICENSE | Permissions |

# Description of the project

I wrote a parser that reads multiple folders of ABC files which in turn identifies each tune inside them and uses that information to insert every tune into a database for analysis.

# Instructions for use

Running full_program.py opens the menu based interface while running gui.py launches the graphical application. Both connect to the same database and analysis functions. Great consistency.

# How it works:
Extracting tune metadata line by line and store the result in a dictionary.
When tunes are identified they get inserted into a database with the book number. The program loads the sotred data into Pandas for analysis.

The GUI is a layer on top of the system to perform search and plot data. 

# Screenshots





# References
* Item 1
* Item 2

# What I am most proud of in the assignment

Storing hundreds of tunes 

# What I learned

Bla bla bla

## Below is how to use Markdown. You can delete this:

## This is how to markdown text:

This is *emphasis*

This is a bulleted list

- Item
- Item

This is a numbered list

1. Item
1. Item

This is a [hyperlink](http://bryanduggan.org)

# Headings
## Headings
#### Headings
##### Headings

This is code:

```Java
public void render()
{
	ui.noFill();
	ui.stroke(255);
	ui.rect(x, y, width, height);
	ui.textAlign(PApplet.CENTER, PApplet.CENTER);
	ui.text(text, x + width * 0.5f, y + height * 0.5f);
}
```

So is this without specifying the language:

```
public void render()
{
	ui.noFill();
	ui.stroke(255);
	ui.rect(x, y, width, height);
	ui.textAlign(PApplet.CENTER, PApplet.CENTER);
	ui.text(text, x + width * 0.5f, y + height * 0.5f);
}
```

This is an image using a relative URL:

![An image](images/p8.png)

This is an image using an absolute URL:

![A different image](https://bryanduggandotorg.files.wordpress.com/2019/02/infinite-forms-00045.png?w=595&h=&zoom=2)

This is a youtube video:

[![YouTube](http://img.youtube.com/vi/J2kHSSFA4NU/0.jpg)](https://www.youtube.com/watch?v=J2kHSSFA4NU)

This is a table:

| Heading 1 | Heading 2 |
|-----------|-----------|
|Some stuff | Some more stuff in this column |
|Some stuff | Some more stuff in this column |
|Some stuff | Some more stuff in this column |

|Some stuff | Some more stuff in this column |

