import string
import spacy
import pandas as pd
import numpy as np

def basic_cleaning(speech):
    speech = speech.replace('\n', ' ')
    speech = ''.join(char for char in speech if not char.isdigit())
    speech = speech.lower()
    for punctuation in string.punctuation:
        speech = speech.replace(punctuation, '')
    speech = speech.strip()
    speech.dropna(inplace=True)

    return speech

# load without NER
nlp = spacy.load("en_core_web_lg", exclude=["ner"])

# source NER from the same pipeline package as the last component
nlp.add_pipe("ner", source=spacy.load('en_core_web_lg'))

# insert the entity ruler
nlp.add_pipe("entity_ruler", before="ner")

def preproc(speeches):
    doc = nlp(speeches)
    stop_words = nlp.Defaults.stop_words
    filtered_tokens = [token.text for token in doc if token.text.lower() not in stop_words]
    lemmas = [token.lemma_ for token in doc if token.text in filtered_tokens]
    # entities = [ent.text for ent in doc.ents]

    return lemmas, # entities
