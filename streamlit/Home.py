import streamlit as st
st.set_page_config(layout="wide", page_title="UN Speeches", page_icon="🌍")

# Social sharing meta tags — replace YOUR_APP_URL with your deployed Streamlit URL
st.markdown("""
<meta property="og:title" content="UN Speeches — 75 Years of Diplomacy">
<meta property="og:description" content="Explore 8,000+ UN General Debate speeches from 1946–2021. Search, map, and compare how 193 countries spoke on 14 global topics using machine learning.">
<meta property="og:image" content="https://YOUR_APP_URL/app/static/preview.png">
<meta property="og:url" content="https://YOUR_APP_URL">
<meta name="twitter:card" content="summary_large_image">
""", unsafe_allow_html=True)

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

with st.expander("📖 Methodology"):
    st.markdown("""
**Dataset**

UN General Debate speeches from the [UN Digital Library](https://digitallibrary.un.org),
covering 1946–2021 across 193 member states. Raw speeches were split into individual
paragraphs using sentence-boundary detection, yielding **117,496 paragraph-level records**.

**Topic Classification**

Paragraphs were embedded using the `all-mpnet-base-v2` model
([Sentence Transformers](https://www.sbert.net)) and classified to one of 15 topics via
**cosine similarity** against hand-authored topic anchor texts. Each paragraph is assigned a
topic and a similarity score. Paragraphs with low similarity across all topics fall into a
catch-all class and are excluded from all visualisations — this filters out generic diplomatic
boilerplate and procedural text.

**UMAP — Speech Similarity Map**

Paragraph embeddings are aggregated to speech level (country × year × topic) and projected
to 2D using [UMAP](https://umap-learn.readthedocs.io) (Uniform Manifold Approximation and
Projection). UMAP preserves local neighbourhood structure — countries placed close together
used similar language when discussing that topic.

**Caveats**

Classification is probabilistic. Speeches before 1970 are sparser. The *Technology AI Cyber*
topic naturally has few matches in early decades. Country name disambiguation is heuristic.

**Team**

Renzo Rico, Teresa Taló & Louis Declée
""")

st.divider()

st.subheader("Start Exploring")

cta_cols = st.columns(4)
cta_links = [
    ("pages/0_🔍_Speech_Search.py",       "🔍 Search Speeches"),
    ("pages/1_🌍_Speech_Map.py",           "🌍 Speech Map"),
    ("pages/2_🚀 _UMAP.py",               "🚀 Speech Similarity"),
    ("pages/3_📈_Topic_trends.py",         "📈 Topic Trends"),
    ("pages/4_🗺️_Mentioned_Countries.py", "🗺️ Mentioned Countries"),
    ("pages/5_📊_Topic_Histogram.py",      "📊 Topic Histogram"),
    ("pages/6_☁️_Word_Cloud.py",          "☁️ Word Cloud"),
]
for i, (path, label) in enumerate(cta_links):
    with cta_cols[i % 4]:
        st.page_link(path, label=label)

st.markdown("""
<div style="text-align:center;padding:24px 0 12px;border-top:1px solid #e0e0e0;margin-top:24px;color:#666;font-size:0.82rem;line-height:2.2;">
  Data sourced from the <a href="https://digitallibrary.un.org" target="_blank" style="color:#009EDB;">UN Digital Library</a> &nbsp;·&nbsp;
  Topic classification by <strong>Renzo Rico, Teresa Taló &amp; Louis Declée</strong> &nbsp;·&nbsp;
  <a href="https://github.com/renzorico/speeches-at-UN" target="_blank" style="color:#009EDB;">GitHub</a>
</div>
""", unsafe_allow_html=True)
