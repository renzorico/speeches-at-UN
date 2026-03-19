import pandas as pd
import streamlit as st
import re
from data import run_query, BIG_QUERY, load_clean_data, USE_LOCAL_MODE


def split_extract(text, keyword):
    escaped = re.escape(keyword)
    match = re.search(r'\b{}\b'.format(escaped), text, flags=re.IGNORECASE)
    if match:
        start_index = match.start()
        end_index = match.end()
        extracted_text = text[max(0, start_index - 300):end_index + 300]
        sentences = re.split(r'(?<=[.!?])\s+', extracted_text)
        keyword_indices = [i for i, sentence in enumerate(sentences) if re.search(r'\b{}\b'.format(escaped), sentence, flags=re.IGNORECASE)]
        if keyword_indices:
            first_sentence_index = max(0, keyword_indices[0] - 1)
            last_sentence_index = min(keyword_indices[-1] + 2, len(sentences))
            return sentences[first_sentence_index:last_sentence_index]


def display_search(search_text, topic, sort_order='Most recent'):
    if st.button("Search"):
        df = load_clean_data()
        if df is not None:
            mask = df['speeches'].str.contains(search_text, case=False, na=False)
            corpus_df = df[mask][['country', 'topic', 'year', 'iso', 'speeches']].copy()
            corpus_df['year_iso'] = corpus_df['year'].astype(str) + ' ' + corpus_df['iso']
            if topic:
                corpus_df = corpus_df[corpus_df['topic'] == topic]
        elif not USE_LOCAL_MODE:
            query = f'''SELECT country, topic, CONCAT(year, ' ', iso) as year_iso, year, country, speeches
                    FROM {BIG_QUERY}
                    WHERE LOWER(speeches) LIKE "% {search_text.lower()} %"
                    OR LOWER(speeches) LIKE "%{search_text.lower()} %"
                    OR LOWER(speeches) LIKE "% {search_text.lower()}."
                    '''
            corpus_df = pd.DataFrame(run_query(query))
            if not corpus_df.empty and topic:
                corpus_df = corpus_df[corpus_df['topic'] == topic]
        else:
            st.warning("No data available.")
            return

        if len(corpus_df) > 0:
            corpus_df['search_result'] = corpus_df['speeches'].apply(lambda x: split_extract(x, search_text))
            corpus_df = corpus_df[corpus_df['search_result'].notna()]

            ascending = sort_order == 'Oldest first'
            corpus_df = corpus_df.sort_values('year', ascending=ascending)

            total = len(corpus_df)
            MAX_RESULTS = 50
            corpus_df = corpus_df.head(MAX_RESULTS)
            order_label = 'oldest' if ascending else 'most recent'
            st.info(f"{total:,} paragraph(s) matched — showing the {min(total, MAX_RESULTS)} {order_label}.")
            i = 1
            for _, each in corpus_df.iterrows():
                list_of_sentences = each['search_result']
                year = str(each['year'])
                country = each['country']
                cleaned = [s for s in list_of_sentences if len(s) > 50]
                joined_text = " ".join(cleaned)
                # Strip any leading partial word/fragment before the first capital letter
                capital_match = re.search(r'[A-Z]', joined_text)
                if capital_match and capital_match.start() > 0:
                    joined_text = joined_text[capital_match.start():]
                highlighted_text = re.sub(
                    r'\b' + re.escape(search_text) + r'\b',
                    lambda m: f'<span style="background-color: #FFFF00"><strong>{m.group()}</strong></span>',
                    joined_text,
                    flags=re.IGNORECASE
                )
                st.markdown(f'''<h5><strong>{i}</strong>. Speech of {country} in <u>{year}</u>:</h5> \n\n -  {highlighted_text}''', unsafe_allow_html=True)
                with st.expander("Show full paragraph"):
                    st.write(each['speeches'])
                i += 1
        else:
            st.warning('This word is not present in any speech.')
