import streamlit as st
st.set_page_config(layout="wide", page_title="UN Speeches")

st.title("UN General Debate Speeches — 75 Years of Diplomacy")

st.markdown("""
Every year since 1946, world leaders gather at the United Nations General Assembly to address the international community.
This app explores **75 years of those speeches** (1946–2021), covering statements from 193 member states.

The corpus contains over **8,000 speeches**, broken into **117,000+ paragraphs** and classified into
14 thematic topics using machine learning (Sentence Transformers + cosine similarity).
""")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Speeches", "8,000+")
with col2:
    st.metric("Paragraphs", "117,496")
with col3:
    st.metric("Years covered", "1946 – 2021")

st.divider()

st.subheader("What can you explore?")

pages = [
    ("🔍 Speech Search", "Full-text search across all speeches with keyword highlighting."),
    ("🌍 Speech Map", "Which countries focused on which topics, year by year."),
    ("🚀 UMAP", "A 2D projection of speech similarity — how close countries are in topic space."),
    ("📈 Topic Trends", "How topics evolve over time globally or for a specific country."),
    ("🗺️ Mentioned Countries", "Which countries were named in speeches, broken down by topic."),
    ("📊 Topic Histogram", "Compare the volume of paragraphs across topics."),
    ("☁️ Word Cloud", "Key vocabulary for any country and year."),
]

for icon_name, description in pages:
    st.markdown(f"**{icon_name}** — {description}")

st.divider()

st.subheader("Topics")
st.markdown("""
Speeches are classified into 14 thematic topics. Paragraphs that don't fit any topic
(generic diplomatic language, procedural text) are excluded from all visualisations.

| Topic | What it covers |
|---|---|
| Peace War Security | Conflicts, ceasefires, arms control, peacekeeping |
| Climate Environment | Climate change, biodiversity, pollution |
| Sustainable Development Poverty | SDGs, development aid, poverty reduction |
| Global Health Pandemics | Health systems, disease, COVID-19 |
| Human Rights Democracy | Rights, judicial systems, governance |
| Gender Equality Inclusion | Women's rights, inclusion, discrimination |
| Migration Refugees Displacement | Displacement, asylum, migration policy |
| Humanitarian Crises | Emergency relief, food security, disaster response |
| Global Economy Trade Debt | Trade, debt, financial systems |
| Multilateralism UN Reform | UN system, multilateral cooperation, reform |
| Decolonization Historical Justice | Colonial history, reparations, self-determination |
| Crime Terrorism Illicit Flows | Terrorism, drug trafficking, cybercrime |
| Technology AI Cyber | Digital technology, AI, cyber security |
| Regional Geopolitical | Regional conflicts, bilateral relations, geopolitics |
""")

st.divider()
st.caption("Data sourced from the UN Digital Library. Speeches harmonized and classified at Le Wagon.")
