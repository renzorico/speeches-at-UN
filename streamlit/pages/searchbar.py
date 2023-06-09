import streamlit as st
import pandas as pd

corpus_path = "~/code/renzorico/speeches-at-UN/raw_data/all_speeches.csv"
corpus_df = pd.read_csv(corpus_path)
corpus_df = corpus_df[['year_iso', 'speeches']]
corpus_df.dropna(subset=['speeches'], inplace=True)

st.title("Speech Search")

search_text = st.text_input("Enter the text to search:")


if st.button("Search"):
    # Filter the corpus for rows containing the search text
    search_results = corpus_df[corpus_df["speeches"].str.contains(search_text, case=False)]

    # Display the search results as a dataframe
    st.write("Search Results:")
    st.dataframe(search_results[["year_iso", "speeches"]])
