import pandas as pd
import streamlit as st
import re
from data import run_query, BIG_QUERY, select_info



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


def display_search(search_text):
    if st.button("Search"):
        # Filter the corpus for rows containing the search text
        query = f'''SELECT CONCAT(year, ' ', iso) as year_iso, year, country, speeches, topic
                FROM {BIG_QUERY}
                WHERE LOWER(speeches) LIKE "% {search_text.lower()} %"
                OR LOWER(speeches) LIKE "%{search_text.lower()} %"
                OR LOWER(speeches) LIKE "% {search_text.lower()}."
                '''

        # Remove None columns
        # Debug country and year selection

        corpus_df = pd.DataFrame(run_query(query))
        # year_range, selected_countries = select_info()
        # filtered_data = corpus_df[(corpus_df['year'] >= year_range[0]) & (corpus_df['year'] <= year_range[1])]

        # if selected_countries:
        #     filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]

        if len(corpus_df) > 0:
            corpus_df['lower_case_text'] = corpus_df.apply(lambda x: x['speeches'].lower(), axis= 1)
            search_results = corpus_df[corpus_df["lower_case_text"].str.contains(search_text.lower(), case=False)]
            search_results['search_result'] =  search_results["speeches"].apply(lambda x: split_extract(x, search_text))
            search_results = search_results.loc[search_results['search_result'] != 'None']

            # Display the search results as a dataframe
            st.write("Search Results:")
            st.dataframe(search_results[["year_iso", "search_result"]])
        else:
            st.warning('This word is not present in any speech.')


            # i = 1
            # for each in search_results.search_result:
            #     st.text(f"{i} {each}")
            #     i += 1
