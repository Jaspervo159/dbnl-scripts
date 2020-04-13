# dbnl-scripts
Scripts to scrape DBNL and work with the texts.

## Requirements
All code is written in Python 3. Libraries that need to be installed:

* SpaCy (including the Dutch model: `nl_core_news_sm`)
* ebooklib
* BeautifulSoup
* Pyphen

## Contents

* `index_dbnl.py` shows how to build an index of the files currently hosted at DBNL.
* `accidental_haiku.py` shows how to detect accidental haikus in an epub file.
* `download_example.py` shows how to download a selection of the DBNL epub books.
* `utils.py` provides useful functions that could be used elsewhere.
