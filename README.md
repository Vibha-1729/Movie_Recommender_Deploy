# 🎬 Movie Recommendation System

A content-based movie recommendation system built using the TMDB 5000 dataset. This project recommends movies by comparing the similarity of their content using text vectorization, stemming, and cosine similarity. The system is deployed as an interactive web application with movie posters fetched dynamically via the TMDB API.

---

## 📌 Overview

This system recommends movies based on their **content similarity**, considering:
- Plot overview  
- Genres  
- Keywords  
- Cast (top 3 actors)  
- Director  

All these attributes are combined into a single textual representation for each movie, enabling the model to identify and suggest movies with similar themes and descriptions.

---

## 🚀 Key Features

- 🎥 Content-based movie recommendations  
- ✂️ Text preprocessing with **stemming**  
- 📊 Bag of Words vectorization (5000 features)  
- 📐 Cosine similarity for matching movies  
- 🖥️ Interactive Streamlit web interface  
- 🖼️ Real-time poster fetching via TMDB API  
- ⚠️ Robust handling of API failures  

---

## 🗂️ Dataset

**TMDB 5000 Movie Metadata**  
📎 Kaggle: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata  

Files used:
- `movies.csv`
- `credits.csv`  

The dataset contains metadata of approximately 5000 movies, including plot summaries, genres, cast, crew, and keywords.

---

## 🔧 Data Preprocessing

High-quality preprocessing is essential for effective content-based recommendations. The following pipeline was implemented:

1. **Data Integration**  
   Merged `movies.csv` and `credits.csv` using the common `title` column to form a unified dataset.

2. **Feature Selection**  
   Retained only the most relevant columns:
   - `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`

3. **Handling Missing Values**  
   Dropped rows with missing values in the `overview` column as missing data was very sparse as compared to the size of the dataset, as plot summaries are critical for capturing movie content.

4. **Parsing Structured Columns**  
   Several fields were stored as lists of dictionaries and were processed as follows:
   - **Genres & Keywords:** Extracted only the `name` values.  
   - **Cast:** Selected the top 3 actors for each movie.  
   - **Crew:** Filtered to keep only the director’s name.

5. **Tokenization & Normalization**  
   - Split the `overview` into individual words.  
   - Converted all text to lowercase for uniformity.

6. **Name Consolidation**  
   Removed spaces from multi-word names (e.g., *Sam Worthington → SamWorthington*) so that names are treated as single unique tokens.

7. **Tag Construction**  
   Created a new column `tags` by concatenating:
   - Overview tokens  
   - Genres  
   - Keywords  
   - Cast names  
   - Director name 

   This resulted in one consolidated textual feature representing each movie.

## 🧠 Methodology

The recommendation engine is built around the idea that movies sharing similar words in their content should be considered similar.

### ➤ Tag-Based Representation
Each movie is represented by a single textual feature called `tags`, created by combining:
- Overview  
- Genres  
- Keywords  
- Cast (top 3 actors)  
- Director  

This `tags` column captures the complete descriptive profile of a movie.

---

### ➤ Text Vectorization (Text → Vector)

To compare movies numerically, the `tags` text is converted into vectors using the **Bag of Words (BoW)** model:

- All tags are combined to build a vocabulary of the **top 5000 most frequent words**.
- Each movie is represented as a vector of length 5000.
- Each element in the vector indicates the presence/frequency of a word in that movie’s tags.

This transforms every movie into a point in a **5000-dimensional vector space**.

---

### ➤ Stemming (Root Word Normalization)

Before vectorization, **stemming** is applied using NLTK to reduce words to their root form.

Examples:
- *actor, actors, acting* → **actor**  
- *love, loved, loving* → **love**

This ensures that different forms of the same word are treated as a single feature, improving similarity matching.

---

### ➤ Similarity Computation

Once vectors are created, **cosine similarity** is used to measure how similar two movies are:

- Cosine similarity measures the angle between two vectors.
- A higher value indicates more similar word distributions in their tags.

For a selected movie:
1. Its similarity score is computed with every other movie.
2. The scores are sorted in descending order.
3. The **top 5 movies** with the highest similarity scores are selected as recommendations.

These top matches are returned as the final recommendations.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Libraries:** Pandas, NumPy, Scikit-learn, NLTK  
- **Web Framework:** Streamlit  
- **Utilities:** Requests, Pickle  
- **API:** TMDB API  

---

## 🌐 Live Demo

🚀 **Deployed Application:**  
👉 https://movie-recommender-deploy-2.onrender.com/

---
