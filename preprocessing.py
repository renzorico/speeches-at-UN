from spacy.lang.en.stop_words import STOP_WORDS
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import string
import spacy
import matplotlib.pyplot as plt
import seaborn as sns

def basic_cleaing(text):
    if isinstance(speech, str):
        speech = ''.join(char for char in speech if not char.isdigit())
        speech = speech.lower()
        for punctuation in string.punctuation:
            speech = speech.replace(punctuation, '')
        speech = speech.strip()
    else:
        speech = ''
    return speech

def preproc(speeches):

    nlp = spacy.load('en_core_web_lg')

    doc = nlp(speeches)

    # tokens = [token.text for token in doc]
    # pos_tags = [(token.text, token.pos_) for token in doc]
    # ner = [(ent.text, ent.label_) for ent in doc.ents]

    filtered_tokens = [token.text for token in doc if not token.is_stop]

    lemmas = [token.lemma_ for token in doc if token.text in filtered_tokens]

    return lemmas
