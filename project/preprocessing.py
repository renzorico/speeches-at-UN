import string
import spacy
import pandas as pd
import numpy as np

def basic_cleaning(speech):
    speech = ''.join(char for char in speech if char.isalpha())
    speech = speech.lower()
    for punctuation in string.punctuation:
        speech = speech.replace(punctuation, '')
    speech = speech.strip()
    return speech

def preproc(speeches):
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(speeches)
    filtered_tokens = [token.text for token in doc if not token.is_stop]
    lemmas = [token.lemma_ for token in doc if token.text in filtered_tokens]
    return lemmas
