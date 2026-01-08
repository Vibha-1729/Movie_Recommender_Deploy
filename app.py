from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st
import pickle
import pandas as pd
import requests
from urllib.parse import quote, unquote
import os

# -----------------------
# Config
# -----------------------
API_KEY = os.getenv("TMDB_API_KEY")

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# Load Data (MEMORY SAFE)
# -----------------------
@st.cache_resource
def load_data():
    movies_list = pickle.load(open("movies_dict.pkl", "rb"))
    movies = pd.DataFrame(movies_list)

    embeddings = pickle.load(open("movie_embeddings.pkl", "rb"))
    embeddings = embeddings.astype("float32")  # 🔥 critical

    return movies, embeddings

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

movies, embeddings = load_data()
model = load_model()

# -----------------------
# Helpers
# -----------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    if not API_KEY:
        return "https://via.placeholder.com/300x450?text=API+Key+Missing"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        path = r.json().get("poster_path")
        if path:
            return f"https://image.tmdb.org/t/p/w500/{path}"
    except:
        pass
    return "https://via.placeholder.com/300x450?text=No+Poster"

@st.cache_data(show_spinner=False)
def fetch_overview_by_title(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": API_KEY, "query": title, "language": "en-US", "page": 1}
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        res = r.json().get("results", [])
        if res:
            return res[0].get("overview", title)
    except:
        pass
    return title

@st.cache_data(show_spinner=False)
def fetch_popular_movies(k=10):
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": API_KEY, "language": "en-US", "page": 1}
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        results = r.json()["results"][:k]
        return [{
            "title": m["title"],
            "poster": f"https://image.tmdb.org/t/p/w500/{m['poster_path']}"
            if m.get("poster_path")
            else "https://via.placeholder.com/300x450?text=No+Poster"
        } for m in results]
    except:
        return []

def clickable_poster(img_url, title):
    encoded = quote(title)
    st.markdown(f"""
    <div class="poster-hover">
        <a href="?clicked={encoded}" target="_self">
            <img src="{img_url}" style="width:100%; border-radius:10px; cursor:pointer;" />
        </a>
        <div style="text-align:center; font-weight:600; margin-top:2px;">{title}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------
# Semantic Search (FIXED)
# -----------------------
def semantic_search(query, k=5):
    q_emb = model.encode([query])   # ✅ real query embedding
    sims = cosine_similarity(q_emb, embeddings)[0]
    top_idx = sims.argsort()[::-1][:k]

    names, posters = [], []
    for i in top_idx:
        movie_id = int(movies.iloc[i].movie_id)
        names.append(movies.iloc[i].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

# -----------------------
# Session State
# -----------------------
if "semantic" not in st.session_state:
    st.session_state.semantic = False
if "query" not in st.session_state:
    st.session_state.query = ""

params = st.query_params
if "clicked" in params:
    title = unquote(params["clicked"])
    st.session_state.query = fetch_overview_by_title(title)
    st.session_state.semantic = True
    st.query_params.clear()

# -----------------------
# Sidebar
# -----------------------
st.sidebar.markdown("## 🎥 Movie Selector")

query = st.sidebar.text_input(
    "🔍 Search by description or movie name",
    value=st.session_state.query,
    placeholder="e.g. time travel, thriller, space adventure..."
)

if st.sidebar.button("Search"):
    st.session_state.query = query
    st.session_state.semantic = True
    st.rerun()

# -----------------------
# Main UI
# -----------------------
st.markdown("""
<h1>🎬 Movie Recommendation System</h1>
<p>✨ Discover movies the smart way!!!\n\n" " Describe a mood, a story, or a movie you loved — or click any poster to explore similar films. MovieRec uses semantic search to understand what you mean and recommends movies that truly match your taste.</p>
""", unsafe_allow_html=True)

# Popular movies
if not st.session_state.semantic:
    popular = fetch_popular_movies(10)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(popular):
            with col:
                clickable_poster(popular[i]["poster"], popular[i]["title"])

# Results
if st.session_state.semantic:
    if st.session_state.query.strip() == "":
        st.warning("Please enter a description or movie name.")
    else:
        with st.spinner("Searching ... 🧠"):
            names, posters = semantic_search(st.session_state.query)

        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i < len(names):
                with col:
                    clickable_poster(posters[i], names[i])
