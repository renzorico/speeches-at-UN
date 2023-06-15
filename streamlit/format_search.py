import pandas as pd
import streamlit as st
import re
from data import run_query, BIG_QUERY



def split_extract(text, keyword):
    match = re.search(r'\b{}\b'.format(keyword), text, flags=re.IGNORECASE)
    # Find the start and end indices of the match
    if match:
        start_index = match.start()
        end_index = match.end()
        # Extract the substring containing the match and the surrounding text
        extracted_text = text[max(0, start_index - 300):end_index + 300]
        sentences = re.split(r'(?<=[.!?])\s+', extracted_text)

        # Find the indices of the sentences that contain the keyword
        keyword_indices = [i for i, sentence in enumerate(sentences) if re.search(r'\b{}\b'.format(keyword), sentence, flags=re.IGNORECASE)]
        if keyword_indices:
            first_sentence_index = max(0, keyword_indices[0] - 1)
            last_sentence_index = min(keyword_indices[-1] + 2, len(sentences))
            selected_sentences = sentences[first_sentence_index:last_sentence_index]
            return selected_sentences


def display_search(search_text, topic):

    if st.button("Search"):

        # Filter the corpus for rows containing the search text
        query = f'''SELECT country, topic, CONCAT(year, ' ', iso) as year_iso, year, country, speeches
                FROM {BIG_QUERY}
                WHERE LOWER(speeches) LIKE "% {search_text.lower()} %"
                OR LOWER(speeches) LIKE "%{search_text.lower()} %"
                OR LOWER(speeches) LIKE "% {search_text.lower()}."
                '''

        corpus_df = pd.DataFrame(run_query(query))
        corpus_df = corpus_df.loc[corpus_df.topic==topic]
        if len(corpus_df) > 0:
            corpus_df['lower_case_text'] = corpus_df.apply(lambda x: x['speeches'].lower(), axis= 1)
            search_results = corpus_df[corpus_df["lower_case_text"].str.contains(search_text.lower(), case=False)]
            search_results['search_result'] =  search_results["speeches"].apply(lambda x: split_extract(x, search_text))
            search_results = search_results.loc[search_results['search_result'] != 'None']
            search_results = search_results.sort_values('year', ascending=False)


            with st.expander("Search Results:", expanded=True):
                i = 1
                for _ , each in search_results.iterrows():
                    list_of_sentences = each['search_result']
                    year = each['year_iso'].split(' ')[0]
                    country = each['country']
                    cleaned = [every for every in list_of_sentences if len(every) > 50 ]
                    joined_text = " ".join(cleaned)
                    highlighted_text = joined_text.replace(search_text, f'<span style="background-color: #FFFF00"><strong>{search_text}</strong></span>')

                    st.markdown(f'''<h5><strong>{i}</strong>. Speech of {country} in <u>{year}</u>:</h5> \n\n -  {highlighted_text}''', unsafe_allow_html=True)
                    i += 1
        else:
            st.warning('This word is not present in any speech.')
