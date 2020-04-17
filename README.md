# dbnl-scripts
Scripts to scrape DBNL and work with the texts ...and to generate a book with accidental haikus.

## Project
I used the code in this repository to generate a book of single-sentence haikus,
automatically collected from DBNL.
 
The [first edition of the book](./book/toevallige-haikus.pdf) has been automatically generated, and typeset in LaTeX. 
LaTeX source code for the book can be found in the `./book/` folder. 
There may or may not be a second, manually curated edition. (At 5,325 pages, this would be a lot of work!)

## Requirements
All code is written in Python 3. Libraries that need to be installed:

* SpaCy (including the Dutch model: `nl_core_news_sm`)
* ebooklib
* BeautifulSoup
* Pyphen
* pylatexenc

Some of the Python syntax only works with versions >= 3.6.

## Contents
There is one python file (`utils.py`) with general-purpose functions.
The other files should be run in the following order, using `python FILENAME.py`:

1. `index_dbnl.py` builds an index of the files currently hosted at DBNL.
2. `download_example.py` downloads a selection of the DBNL epub books.
3. `accidental_haiku.py` detects accidental haikus in the downloaded epub files.
4. `generate_chapters.py` produces chapters for a book exhibiting all accidental haikus.

## Using this code for other projects
The first two Python scripts (`index_dbnl.py` and `download_example.py`) are 
probably useful for other projects as well.
Building an index of DBNL means you can search the database locally, which is 
much faster than scraping the website.
The download script shows how to download epub books. The script can easily be 
modified to your needs.
The other two files are more specific to this project, but they might be useful 
to see how the functions in `utils.py` can be used to read text in .epub files, 
for example.
