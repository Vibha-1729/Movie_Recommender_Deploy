# 🎬 Movie Recommendation System

A content-based movie recommendation system built using the TMDB 5000 dataset. This project leverages Natural Language Processing (NLP) techniques and cosine similarity to recommend movies similar to a user-selected title. An interactive web interface is provided using Streamlit, with real-time movie posters fetched via the TMDB API.

---

## 🌐 Live Demo

🚀 **Deployed Application:**  
👉 https://your-deployed-link-here  

> Replace this with your actual deployed URL (Render / Streamlit Cloud / etc.)

---

## 📌 Overview

This system recommends movies based on their **content similarity**, considering:
- Plot overview  
- Genres  
- Keywords  
- Cast (top 3 actors)  
- Director  

Each movie is represented as a vector in a high-dimensional feature space, and recommendations are generated using cosine similarity.

---

## 🚀 Features

- 🎥 Content-based movie recommendations  
- 🧠 NLP preprocessing with stemming  
- 📊 Bag of Words vectorization (5000 features)  
- 📐 Cosine similarity for matching movies  
- 🖥️ Interactive UI using Streamlit  
- 🖼️ Movie posters via TMDB API  
- ⚠️ Graceful handling of API failures  

---

## 🗂️ Dataset

**TMDB 5000 Movie Metadata**  
📎 Kaggle Link: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata  

Files used:
- `movies.csv`
- `credits.csv`

Contains metadata of ~5000 movies including genres, overview, cast, crew, and keywords.

---

## 🔧 Data Preprocessing

The following steps were performed to prepare the data:

1. Merged `movies.csv` and `credits.csv` on `title`
2. Selected relevant columns:
   - `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`
3. Dropped rows with missing overviews
4. Extracted:
   - Genre names from dictionaries  
   - Keyword names  
   - Top 3 cast members  
   - Director from crew  
5. Tokenized overview text into words
6. Removed spaces in names (e.g., *SamWorthington*) to avoid ambiguity
7. Combined all features into a single **`tags`** column
8. Converted all text to lowercase

Final dataframe structure:
