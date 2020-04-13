import pyphen
import spacy
from utils import get_text, detokenize

dic = pyphen.Pyphen(lang='nl_NL')

def count_syllables(token):
    "Count the number of syllables in a token."
    if token.is_punct:
        return 0
    hyphenated = dic.inserted(token.orth_)
    syllables = hyphenated.split('-')
    return len(syllables)


def check_haiku(sentence):
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

################################################################################
# This does the actual work:

nlp = spacy.load('nl_core_news_sm')
text = get_text('viss012leve01_01.epub')
doc = nlp(text)
print("Start!")
for sent in doc.sents:
    haiku = check_haiku(sent)
    if haiku:
        print(haiku)
