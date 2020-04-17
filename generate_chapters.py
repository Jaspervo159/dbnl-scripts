import json
from collections import defaultdict
from operator import itemgetter
from pylatexenc.latexencode import unicode_to_latex
from string import ascii_lowercase
from functools import partial


GETALLEN  = {1: 'een',
             2: 'twee',
             3: 'drie',
             4: 'vier',
             5: 'vijf',
             6: 'zes',
             7: 'zeven',
             8: 'acht',
             9: 'negen',
             10: 'tien',
             11: 'elf',
             12: 'twaalf',
             13: 'dertien',
             14: 'veertien',
             20: 'twintig',
             30: 'dertig',
             40: 'veertig',
             50: 'vijftig',
             60: 'zestig',
             70: 'zeventig',
             80: 'tachtig',
             90: 'negentig',
             100: 'honderd',
             1000: 'duizend'}

def number_to_word(number):
    """
    Convert integers to a fully written out Dutch number.
    Works for integers up to (but not including) 1,000,000.
    """
    if number in GETALLEN:
        return GETALLEN[number]
    last_digit = number % 10
    tens = number // 10
    hundreds = number // 100
    thousands = number // 1000
    if number < 20:
        return GETALLEN[last_digit] + 'tien'
        
    if number < 100:    
        if last_digit in {2,3}:
            return f"{GETALLEN[last_digit]}ën{GETALLEN[tens * 10]}"
        else:
            return f"{GETALLEN[last_digit]}en{GETALLEN[tens * 10]}"
    
    if number < 200:
        return f"honderd{number_to_word(number - 100)}"
    
    if number % 100 == 0:
        return f"{number_to_word(hundreds)}honderd"
    
    if number < 1000:
        rounded_down = hundreds * 100
        return f"{number_to_word(rounded_down)}{number_to_word(number - rounded_down)}"
    
    if number % 1000 == 0:
        return f"{number_to_word(thousands)}duizend"
    
    if number < 1100:
        return f"duizend{number_to_word(number-1000)}"
    
    if number < 2000:
        rounded_down = hundreds * 100
        return f"{number_to_word(hundreds)}honderd{number_to_word(number-rounded_down)}"
    
    else:
        rounded_down = thousands * 1000
        return f"{number_to_word(thousands)}duizend{number_to_word(number - rounded_down)}"


def alphabetize(entries):
    "Sort the entries by alphabet, so that it's easier to print them."
    entries = sorted(entries, key=itemgetter('id'))
    beginletters = {entry['id'][0] for entry in entries}
    index = {letter: defaultdict(list) for letter in beginletters}
    for entry in entries:
        beginletter = entry['id'][0]
        index[beginletter][entry['auteur']].append(entry)
    index['varia'] = index['_']
    del index['_']
    return index


def fragments_for_entry(entry):
    "Generate LaTeX for a specific entry."
    title = unicode_to_latex(entry['title'])
    fragments = [f"\\subsection{{Uit: {title}}}"]
    for line1, line2, line3 in entry['haikus']:
        command = f"\\haiku{{{line1}}}{{{line2}}}{{{line3}}}\\\\"
        fragments.append(command)
    return fragments


def text_for_auteur(auteur, entries):
    "Generate LaTeX for a specific auteur."
    auteur = unicode_to_latex(auteur)
    fragments = [f"\\section{{{auteur}}}"]
    for entry in entries:
        fragments.extend(fragments_for_entry(entry))
    latex = '\n\n'.join(fragments)
    return latex

# Algemene index:
# {'a': {"Naam Achternaam": [entries]}}
def text_for_letter(letter, letter_index):
    "Generate LaTeX for a specific letter"
    num_authors = len(letter_index.keys())
    num_haikus = sum(len(entry['haikus']) for entries in letter_index.values()
                                              for entry in entries)
    fragments = [f"\\chapter[{num_authors} auteurs, {num_haikus} haiku's]{{{number_to_word(num_authors)} auteurs, {number_to_word(num_haikus)} haiku's}}"]
    for auteur, entries in letter_index.items():
        fragments.append(text_for_auteur(auteur, entries))
    latex = '\n\n'.join(fragments) + '\n'
    return latex


def write_chapters(ordered):
    "Write chapter contents to files."
    for letter,letter_index in ordered.items():
        path = f'./book/chapters/{letter}.tex'
        with open(path, 'w') as f:
            latex = text_for_letter(letter, letter_index)
            f.write(latex)
        print('Written file:', path)
            

def load_haiku_data():
    with open('haikus.json') as f:
        data = json.load(f)
    entries = []
    for entry in data.values():
        entry['auteur'] = entry['auteur'].strip()
        entries.append(entry)
    return entries


def preprocess_entries(entries):
    """
    Preprocess entries, ensuring that the haikus for each entry can be printed.
    If it cannot be typeset by LaTeX, we won't use it.
    """
    results = []
    for entry in entries:
        processed_haikus = []
        for haiku in entry['haikus']:
            try:
                haiku = list(map(partial(unicode_to_latex, unknown_char_policy='fail'), haiku))
                processed_haikus.append(haiku)
            except ValueError:
                print('Skipping haiku')
        entry['haikus'] = processed_haikus
        if not len(processed_haikus) == 0:
            results.append(entry)
    return results


if __name__ == "__main__":
    entries = load_haiku_data()
    entries = preprocess_entries(entries)
    ordered = alphabetize(entries)
    write_chapters(ordered)
