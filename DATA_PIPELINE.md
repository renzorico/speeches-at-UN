# Data Pipeline — UN General Debate Speeches

This document explains how the raw UN speech data is processed from its original form into the datasets powering the Streamlit app.

---

## Overview

```
raw speeches (all_speeches.csv)
        │
        ▼
  1. Harmonization
  2. Text Cleaning
  3. Paragraph Splitting
  4. TF-IDF Vectorization
  5. GPT Topic Classification
        │
        ▼
  speeches_paragraphs.csv        ← main dataset (117,496 rows)
  raw_data/topic_labels.csv ← topic metadata (14 topics)
  streamlit/speeches_umap.csv       ← pre-computed UMAP embeddings
        │
        ▼
  Streamlit App (6 pages)
```

---

## Step 1 — Raw Data

**File:** `data/all_speeches.csv`

This is the original dataset downloaded from the [UN General Debate Corpus](https://doi.org/10.7910/DVN/0TJX8Y), which contains full-text speeches delivered at the UN General Debate from 1946 to 2021.

Each row is one speech by one country in one year. Key columns in the raw file:

| Column | Description |
|---|---|
| `iso` | ISO 3-letter country code |
| `Country` | Country name (inconsistent across years) |
| `speeches` | Full speech text |
| `year` | Year of the speech |
| `session` | UN session number |

---

## Step 2 — Harmonization (`project/data.py`)

The raw data has inconsistencies that are fixed by `harmonize_data()`:

- **Drops unnecessary columns:** `Year`, `Session`, `index`, `year_iso`, `ISO Code`, unnamed columns.
- **Resolves duplicate ISO codes:** Some ISO codes (e.g. `BLR`, `RUS`, `UKR`, `COG`) appear with multiple country name variants across different years. Each is normalized to a single canonical name:
  - `BLR` → `Belarus`
  - `RUS` → `Russia`
  - `UKR` → `Ukraine`
  - `COG` → `Democratic Republic of Congo`
  - `CSK`/`CZK` → `Czechoslovakia`
  - `.DS` rows (filesystem artifact) are dropped.

---

## Step 3 — Text Cleaning (`project/preprocessing.py`)

Each speech text goes through `basic_cleaning()`:

1. Replace `\n` newlines with spaces.
2. Remove all digits.
3. Lowercase the entire string.
4. Remove all punctuation.
5. Strip leading/trailing whitespace.

This produces a clean text string (`cleaned_speeches`) suitable for vectorization.

---

## Step 4 — Paragraph Splitting

Speeches are long documents (often many pages). To get more granular topic assignments, each speech is split into individual paragraphs. This is the key step that transforms the data from **speech-level** (one row per speech) to **paragraph-level** (one row per paragraph).

- Input: ~8,000 speeches
- Output: **117,496 paragraphs** — each row in `speeches_paragraphs.csv`

Short or empty paragraphs are discarded. The original speech text and the cleaned version are both preserved.

---

## Step 5 — TF-IDF Vectorization (`project/tfidf.py`)

Each paragraph is vectorized using `TfidfVectorizer` from scikit-learn:

- **N-grams:** bigrams and trigrams (`ngram_range=(2, 3)`)
- **Max features:** 2,000 most frequent n-grams
- **Stop words:** standard English stop words removed

This produces a TF-IDF matrix that highlights the most characteristic multi-word phrases in each paragraph. The top 5 phrases per paragraph are stored as `top_5_words`.

---

## Step 6 — GPT Topic Classification

This is the most important step. The TF-IDF top phrases for each paragraph were sent to GPT in batches with a structured prompt, asking GPT to assign one of **14 predefined topic labels**:

| Topic | Description |
|---|---|
| `war` | Armed conflict, military operations, peace negotiations |
| `climate` | Climate change, greenhouse gases, renewable energy |
| `multilateralism` | UN reform, international cooperation, multilateral institutions |
| `development` | Development goals, poverty, sustainable development |
| `disarmament` | Nuclear weapons, arms control, non-proliferation |
| `decolonization` | Colonial history, independence movements, apartheid |
| `terrorism` | Counter-terrorism, extremism, security threats |
| `migration_refugees` | Refugee crises, displacement, asylum |
| `humanitarian crises` | Humanitarian aid, disaster response |
| `human_rights` | Human rights law, political rights, civil liberties |
| `drugs_crime` | Drug trafficking, illicit substances, organized crime |
| `pandemic_health` | COVID-19, public health, WHO, disease outbreaks |
| `gender_issues` | Gender equality, women's rights, girls' education |
| `economic` | Trade, economic reform, financial institutions |
| `bla_bla` | Generic/procedural text with no meaningful topic — **excluded from the app** |

Each paragraph gets exactly one label. The `bla_bla` category (38,750 rows) acts as a catch-all for boilerplate text ("I welcome this assembly", "As my delegation stated…") and is filtered out in all visualizations.

The intermediate GPT prompt files (`Topics_prompt_GPTtext*.csv`) were working artifacts from this process and are not needed after the labels were applied to the dataset.

---

## Step 7 — Country Mentions Extraction

Within each paragraph, mentions of other countries are extracted using Named Entity Recognition (NER). These raw mentions are then normalized using `streamlit/clean_countries.py` — a lookup table that maps historical country names, abbreviations, and common variants to standardized names:

- `the Soviet Union` → `Russia`
- `Viet Nam` / `Viet-Nam` → `Vietnam`
- `the United States` / `America` → `United States of America`
- `the United Kingdom` / `Britain` / `Great Britain` → `United Kingdom`
- Cities and non-country entities (Geneva, New York, Jerusalem…) are excluded.

The result is stored in two columns:
- `countries_mentioned` — raw extracted strings
- `countries_recoded` — normalized list stored as a Python list string, e.g. `"['Syria', 'Jordan']"`

---

## Step 8 — Final Dataset (`data/speeches_paragraphs.csv`)

The canonical dataset used by the Streamlit app. **117,496 rows, paragraph level.**

| Column | Type | Description |
|---|---|---|
| `iso` | str | ISO 3-letter country code |
| `year` | int | Year of the speech |
| `country` | str | Normalized country name |
| `speeches` | str | Original full paragraph text |
| `cleaned_speeches` | str | Cleaned (lowercase, no punctuation) |
| `preprocessed_speech` | str | Further preprocessed version |
| `topic` | str | One of 14 topic labels (or `bla_bla`) |
| `top_5_words` | str | Top TF-IDF phrases for this paragraph |
| `countries_mentioned` | str | Raw NER country mentions |
| `countries_recoded` | str | Normalized country list (parse with `ast.literal_eval`) |
| `continent` | str | Continent of the speaking country |
| `decade` | str | Decade of the speech (e.g. `1990s`) |
| `year_range` | str | 5-year range bucket |

> **Note:** `countries_recoded` is stored as a stringified Python list. To use it:
> ```python
> import ast
> df['countries_recoded'] = df['countries_recoded'].apply(
>     lambda x: ast.literal_eval(x) if pd.notna(x) and x != '[]' else []
> )
> ```

---

## Step 9 — Topic Metadata (`raw_data/topic_labels.csv`)

A small summary table (14 rows) extracted from `speeches_paragraphs.csv` containing:

| Column | Description |
|---|---|
| `topic_id` | Numeric ID |
| `topic_name` | Topic label string |
| `count` | Number of paragraphs with this topic |
| `top_5_words` | Representative TF-IDF phrases for this topic |

Used by the app to populate topic dropdowns and filter menus without loading the full 528 MB dataset.

---

## Step 10 — UMAP Embeddings (`streamlit/speeches_umap.csv`)

Pre-computed 2D UMAP projections at **speech level** (44,542 rows, one per speech).

The text embeddings (sentence transformers or similar) were reduced to 2 dimensions using UMAP, then saved to CSV to avoid recomputing at runtime.

| Column | Description |
|---|---|
| `iso` | Country ISO code |
| `year` | Year |
| `country` | Country name |
| `continent` | Continent |
| `topic` | Topic label |
| `umap_1` | First UMAP dimension |
| `umap_2` | Second UMAP dimension |
| `count` | Number of paragraphs in this speech |

> The topic set in `speeches_umap.csv` differs slightly from `speeches_paragraphs.csv` (it predates the final GPT classification). The UMAP page reads topics directly from `speeches_umap.csv` to avoid mismatches.

---

## Streamlit App Pages

The app loads data from `speeches_paragraphs.csv` (local mode) or BigQuery (cloud mode) with a local-first, BigQuery-fallback pattern.

| Page | Source data | What it shows |
|---|---|---|
| **Home** — Speech Search | `speeches_paragraphs.csv` | Full-text search across all paragraphs, filtered by topic |
| **1 — Speech Map** | `speeches_paragraphs.csv` (aggregated) | Choropleth map of speech counts by country, topic, and year range |
| **2 — UMAP** | `speeches_umap.csv` | 2D scatter of speech embeddings, colored by continent |
| **3 — Topic Trends** | `speeches_paragraphs.csv` (aggregated) | Line chart of topic frequency over time, by country |
| **4 — Mentioned Countries** | `speeches_paragraphs.csv` (aggregated) | Choropleth map of which countries are most mentioned, filtered by topic/year |
| **5 — Topic Histogram** | `speeches_paragraphs.csv` + `topic_labels.csv` | Bar chart of paragraph counts per topic |
| **6 — Word Cloud** | `speeches_paragraphs.csv` (grouped by year+country) | Word cloud of most frequent terms |

---

## Reproducing the Pipeline

To re-run the pipeline from scratch (you will need `data/all_speeches.csv`):

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the pipeline (harmonize → clean → classify → output)
cd project
python main.py
```

Output files written to:
- `raw_data/clean_data.csv` — cleaned paragraphs with topic assignments
- `raw_data/topic_labels.csv` — topic metadata

> **Note:** The production `speeches_paragraphs.csv` was produced using a GPT-assisted classification step (Step 6) that is not fully automated in `main.py` as it currently stands. `main.py` runs BERTopic as a stand-in; the 14-topic GPT labels in `speeches_paragraphs.csv` were assigned in a separate interactive session using the `Topics_prompt_GPTtext` files.
