"""
Example script to download a selection of files from DBNL.

This script downloads:
- all documents after 1900, 
- that are exclusively marked as 'proza',
- and that are available in epub format.
"""

from utils import load_dbnl_data
import time
import urllib.request
import os

def select(data, 
           genres, 
           exact=False, 
           year_start=0, 
           year_end=3000,
           need_epub=True,
           need_pdf=True):
    "Select books from DBNL."
    results = []
    genres = set(genres)
    for entry in data:
        if not genres.issubset(entry['genres']):
            continue
        if exact and not genres == entry['genres']:
            continue
        if need_epub and not 'epub' in entry['download']:
            continue
        if need_pdf and not 'pdf' in entry['download']:
            continue
        # Warning: only works for entries where exact year is specified!
        if not entry['year'].isdigit():
            continue
        if year_start <= int(entry['year']) <= year_end:
            results.append(entry)
    return results


def download(url, folder):
    "Download file to a folder."
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = url.split('/')[-1]
    urllib.request.urlretrieve(url, folder + filename)


def download_entry(entry, folder):
    "Download entry to a folder."
    download(entry['download']['epub'], folder)


data = load_dbnl_data()    
selection = select(data, ['proza'], exact=True, year_start=1900)

for entry in selection:
    download_entry(entry, './proza/')
    time.sleep(2) # Be nice to DBNL
