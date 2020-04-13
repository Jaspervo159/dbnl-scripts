from string import punctuation
PUNCTUATION = set(punctuation)
import pyphen

import spacy

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def get_text(filename):
    "Get text from an epub file."
    book = epub.read_epub(filename)
    texts = []
    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = doc.content
        soup = BeautifulSoup(content, features="lxml")
        texts.append(soup.text)
    return('\n'.join(texts))

dic = pyphen.Pyphen(lang='nl_NL')

def count_syllables(token):
    "Count the number of syllables in a token."
    if token in PUNCTUATION:
        return 0
    hyphenated = dic.inserted(token)
    syllables = hyphenated.split('-')
    return len(syllables)

def check_haiku(sentence):
    first, second, third = 0, 0, 0
    first_line = []
    second_line = []
    third_line = []
    for token in sentence:
        token = token.orth_
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
    first_line = ' '.join(first_line)
    second_line = ' '.join(second_line)
    third_line = ' '.join(third_line)
    return first_line, second_line, third_line
        

nlp = spacy.load('nl_core_news_sm')

text = get_text('viss012leve01_01.epub')
doc = nlp(text)
print("Start!")
for sent in doc.sents:
    haiku = check_haiku(sent)
    if haiku:
        print(haiku)
