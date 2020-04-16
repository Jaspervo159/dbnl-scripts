import glob
import json
import pyphen
import spacy
from utils import get_text, detokenize, load_dbnl_data, chunks, store_dbnl_data
from multiprocessing import Pool
from itertools import repeat

dic = pyphen.Pyphen(lang='nl_NL')

def count_syllables(token):
    "Count the number of syllables in a token."
    if token.is_punct:
        return 0
    hyphenated = dic.inserted(token.orth_)
    syllables = hyphenated.split('-')
    return len(syllables)


def check_haiku(sentence):
    """
    Checks whether is a sentence fits the (simplified) criteria for a haiku.
    """
    first, second, third = 0, 0, 0
    first_line = []
    second_line = []
    third_line = []
    for token in sentence:
        syllables = count_syllables(token)
        if first < 5:
            first += syllables
            first_line.append(token)
        elif second < 7:
            if syllables == 0:
                first_line.append(token)
            else:
                second += syllables
                second_line.append(token)
        else:
            if syllables == 0:
                first_line.append(token)
            else:
                third += syllables
                third_line.append(token)
    if any([first != 5, second != 7, third != 5]):
        return None
    first_line = detokenize(first_line)
    second_line = detokenize(second_line)
    third_line = detokenize(third_line)
    return first_line, second_line, third_line


nlp = spacy.load('nl_core_news_sm')

def haikus_for_document(filename):
    """
    Analyzes a document for haikus. Returns a list of tuples.
    """
    text = get_text(filename)
    haikus = []
    # SpaCy has a maximum text size of 1,000,000 characters.
    # Let's use one fewer to be on the safe side.
    for chunk in chunks(text,999_999): # this underscore syntax was introduced in Python 3.6
        doc = nlp(chunk)
        for sent in doc.sents:
            haiku = check_haiku(sent)
            if haiku:
                haikus.append(haiku)
    return haikus


def haikus_for_documents(paths):
    """
    Extract haikus from all documents, update the index, 
    and return list of filenames of processed files.
    
    This function provides a single-threaded alternative to haiku_multiprocessing.
    """
    results = []
    total_haikus = 0
    for i, path in enumerate(paths,start=1):
        filename = path.split('/')[-1]
        haikus = haikus_for_document(path)
        results.append((filename, haikus))
        total_haikus += len(haikus)
        print(f"File {i}/{len(paths)}. Total number of haikus: {total_haikus}")
    return results


def single_process(path):
    "Helper function for the multiprocessing function."
    filename = path.split('/')[-1]
    haikus = haikus_for_document(path)
    print(f"Processed file: {filename}. Found {len(haikus)} haikus.")
    return filename, haikus


def haiku_multiprocessing(paths, num_processes=2):
    """
    Extract haikus from all documents, update the index, 
    and return list of filenames of processed files.
    """
    with Pool(num_processes) as pool:
        results = pool.map(single_process, paths)
    return results


def compile_results(results, index):
    "Compile results in a dictionary."
    selection = dict()
    for filename, haikus in results:
        selection[filename] = index[filename]
        selection[filename]['haikus'] = haikus
    return selection

################################################################################
# This does the actual work:

if __name__ == "__main__":
    data = load_dbnl_data()
    index = {entry['download']['epub'].split('/')[-1]: entry for entry in data 
                                                             if 'epub' in entry['download']}
    
    # This only works if there is a ./proza/ folder, with .epub files in it.
    paths = glob.glob('./proza/*.epub')
    # filenames = haikus_for_documents(paths, index)
    results = haiku_multiprocessing(paths, num_processes=2)
    selection = compile_results(results, index)
    store_dbnl_data(selection, 'haikus.json')
