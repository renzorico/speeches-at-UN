import pandas as pd
import streamlit as st
import re
import numpy as np

def load_search_data():
    corpus_path = "/root/code/renzorico/speeches-at-UN/raw_data/all_speeches.csv"
    corpus_df = pd.read_csv(corpus_path)
    corpus_df = corpus_df[['year_iso', 'speeches']]
    return corpus_df.dropna(subset=['speeches'])

def split_extract(text, keyword):
    # Find the start and end indices of the keyword occurrence in the text
    match = re.search(r'\b{}\b'.format(keyword), text, flags=re.IGNORECASE)
    if match:
        start_index = max(0, match.start() - 100)
        end_index = min(len(text), match.end() + 100)
        extracted_text = text[start_index:end_index]
        # Add paragraph number to the extracted text
        extracted_text = f'Occurrence 1\n{extracted_text}'
        return extracted_text
    return 'None'

def display_search(corpus_df, search_text):
    if st.button("Search"):
        # Filter the corpus for rows containing the search text
        corpus_df['lower_case_text'] = corpus_df['speeches'].apply(lambda x: x.lower())
        search_results = corpus_df[corpus_df["lower_case_text"].str.contains(search_text.lower(), case=False)]
        search_results['search_result'] =  search_results["speeches"].apply(lambda x: split_extract(x, search_text))
        search_results = search_results.loc[search_results['search_result'] != 'None']

        # Display the search results as a dataframe
        st.write("Search Results:")
        st.dataframe(search_results[["year_iso", "search_result", "speeches"]])
