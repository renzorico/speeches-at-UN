import streamlit as st
from topicplot import display_topics, select_topic_hist


def hist_main():
    display_topics()
    result = select_topic_hist()
    if result:
        words_list, count = result
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Paragraphs in topic", f"{count:,}")
        with col2:
            st.markdown("**Top keywords**")
            tags = " ".join([
                f'<span style="background-color:#e8f4ea; padding:4px 12px; border-radius:12px; margin:3px; display:inline-block;">{w}</span>'
                for w in words_list
            ])
            st.markdown(tags, unsafe_allow_html=True)


hist_main()
