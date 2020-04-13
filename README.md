# dbnl-scripts
Scripts to scrape DBNL and work with the texts.

## Requirements
All code is written in Python 3. Libraries that need to be installed:

* SpaCy (including the Dutch model: `nl_core_news_sm`)
* ebooklib
* BeautifulSoup
* Pyphen

Some of the Python syntax only works with versions >= 3.6.

## Contents

There is one python file (`utils.py`) with general-purpose functions.
The other files should be run in the following order, using `python FILENAME.py`:

1. `index_dbnl.py` builds an index of the files currently hosted at DBNL.
2. `download_example.py` downloads a selection of the DBNL epub books.
3. `accidental_haiku.py` detects accidental haikus in the downloaded epub files.
4. ...

## Project
The current goal of this repository is to generate a book of single-sentence haikus,
automatically collected from DBNL. 
The first edition of the book will be automatically generated, and typeset in LaTeX.
There may or may not be a second, manually curated edition.
