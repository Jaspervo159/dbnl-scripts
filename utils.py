import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

################################################################################
# Load text from epub.

def get_text(filename):
    "Get text from an epub file."
    book = epub.read_epub(filename)
    texts = []
    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = doc.content
        soup = BeautifulSoup(content, features="lxml")
        text = soup.text.replace('\n', ' ')
        texts.append(text)
    return(' '.join(texts))

################################################################################
# To deal with SpaCy's tokenization.

def has_pre_space(token):
    """
    Function to check whether a token has a preceding space.
    
    See: https://stackoverflow.com/a/50330877/2899924
    """
    if token.i == 0:
        return False
    if token.nbor(-1).whitespace_:
        return True
    else:
        return False

def detokenize(tokens):
    "Detokenize sequence of SpaCy tokens."
    sentence = []
    for token in tokens:
        if has_pre_space(token):
            sentence.append(' ')
        sentence.append(token.orth_)
    return ''.join(sentence).strip()
