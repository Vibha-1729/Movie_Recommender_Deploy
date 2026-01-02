# 🎬 Movie Recommendation System

A **semantic movie recommendation system** built using the **TMDB 5000 Movie Dataset**.  
The system enables **natural language–based movie discovery** by encoding movie descriptions into dense vector embeddings and retrieving similar movies using cosine similarity.

It is deployed as an interactive **Streamlit web application** with real-time movie posters fetched dynamically via the **TMDB API**.

---

## 📌 Overview

This project allows users to discover movies in an intuitive way by:

- Searching using **free-text queries** (mood, plot, theme, or story)
- Clicking on any movie poster to explore **similar films**
- Finding movies beyond rigid genre-based filtering

Instead of keyword matching, the system uses **transformer-based semantic embeddings** to understand the *meaning* of both user queries and movie descriptions.

---

## 🚀 Key Features

- 🎥 **Semantic movie recommendations** using transformer embeddings  
- 🧠 Natural language search (e.g. *“time travel love story”*)  
- 📐 **Cosine similarity–based retrieval** in embedding space  
- 🖥️ Interactive and responsive **Streamlit web interface**  
- 🖼️ Real-time poster fetching via **TMDB API**  
- ⚡ Optimized performance using **Streamlit caching**  
- 🛡️ Robust handling of missing posters and API failures  

---

## 🗂️ Dataset

**TMDB 5000 Movie Metadata**  
📎 Kaggle: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata  

**Files used:**
- `movies.csv`
- `credits.csv`

The dataset contains metadata for ~5000 movies, including:
- Plot overviews  
- Genres  
- Cast and crew  
- Keywords  

---

## 🔧 Data Preparation

The following preprocessing steps were applied:

1. **Data Integration**  
   Merged `movies.csv` and `credits.csv` using the movie title.

2. **Feature Selection**  
   Retained relevant attributes such as:
   - Movie ID  
   - Title  
   - Overview  

3. **Text Consolidation**  
   Movie overviews were used as the primary semantic signal for representation learning.

4. **Embedding Generation**  
   Each movie overview was encoded into a dense vector using a pre-trained transformer model.

5. **Embedding Storage**  
   Precomputed embeddings were serialized using `pickle` for fast inference during deployment.

---

## 🧠 Methodology

### ➤ Transformer-Based Embeddings

Each movie is represented as a **dense semantic vector** using a pre-trained sentence transformer:

- **Model:** `all-MiniLM-L6-v2`  
- **Library:** `sentence-transformers`

This approach captures semantic meaning rather than relying on exact word matches, allowing more flexible and intelligent recommendations.

---

### ➤ Semantic Search Pipeline

When a user enters a query:

1. The query is encoded into an embedding using the same transformer model.
2. **Cosine similarity** is computed between the query embedding and all movie embeddings.
3. Movies are ranked by similarity score.
4. The **top-k most similar movies** are returned as recommendations.

This enables searches like:
- *“dark psychological thriller”*
- *“feel good animated movie”*
- *“epic fantasy war movie”*

---

## 🖥️ Web Application

The recommendation engine is deployed as a **Streamlit web app** with:

- Sidebar-based text search
- Clickable movie posters
- URL-based query state handling
- Cached model loading and API calls to reduce latency
- Clean, responsive UI with custom styling

---

## 🛠️ Tech Stack

- **Language:** Python  
- **ML / NLP:** SentenceTransformers, Scikit-learn  
- **Data Processing:** Pandas, NumPy  
- **Web Framework:** Streamlit  
- **Utilities:** Requests, Pickle  
- **API:** TMDB API  

---


## 🌐 Live Demo

🚀 **Deployed Application:**  
👉 [https://movie-recommender-deploy-2.onrender.com/](https://movie-recommender-deploy-3.onrender.com/)

---
