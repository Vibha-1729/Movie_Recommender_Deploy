from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st
import pickle
import pandas as pd
import requests
from urllib.parse import quote, unquote

# -----------------------
# Config
# -----------------------

API_KEY = "31050b1b338785a5b9e64d97a930ecf3"

# import os

# API_KEY = os.getenv("TMDB_API_KEY")


st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.main .block-container {
    padding-top: 0.4rem !important;
    padding-bottom: 0.4rem !important;
}
div[data-testid="stVerticalBlock"] > div {
    gap: 0.3rem !important;
}
div[data-testid="stSpacer"] {
    display: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
    height: 2.5rem !important;
    min-height: 2.5rem !important;
    padding: 0 !important;
}

/* ===============================
   MAIN CONTENT
================================ */
section.main {
    padding-top: 0.2rem !important;
}

/* ===============================
   APP BACKGROUND
================================ */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(1200px at 20% 10%, rgba(99,102,241,0.18), transparent 40%),
        radial-gradient(900px at 80% 30%, rgba(236,72,153,0.15), transparent 40%),
        linear-gradient(180deg, #0b0f19 0%, #020617 100%) !important;
}
section.main, .block-container {
    background: transparent !important;
}

/* ===============================
   SIDEBAR
================================ */
[data-testid="stSidebar"] {
    position: sticky !important;
    top: 0;
    height: 100vh !important;
    overflow-y: auto !important;
    background: linear-gradient(180deg, #111827 0%, #1f2933 100%) !important;
    padding: 0.7rem 0.9rem !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f9fafb !important;
    margin: 0.4rem 0 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #d1d5db !important;
    margin: 0.25rem 0 !important;
}

/* Sidebar inputs */
[data-testid="stSidebar"] input {
    background-color: #0f172a !important;
    color: #f9fafb !important;
    border-radius: 8px !important;
    border: 1px solid #374151 !important;
    padding: 0.5rem !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
    font-weight: 600 !important;
    width: 100% !important;
}

[data-testid="stSidebar"] button:hover {
    background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
}

/* ===============================
   TEXT + HEADINGS
================================ */
h1, h2, h3 {
    margin: 0.4rem 0 !important;
    line-height: 1.15 !important;
}
.stMarkdown p {
    margin: 0.25rem 0 !important;
    color: #c7cbd1 !important;
}

/* ===============================
   POSTER HOVER EFFECT
================================ */
.poster-hover img {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.poster-hover img:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 12px 28px rgba(0,0,0,0.55);
}
            
/* ===============================
   SIDEBAR FOOTER (CENTERED)
================================ */
.sidebar-footer {
    text-align: center !important;
    font-size: 0.8rem !important;
    color: #9ca3af !important;
    margin-top: 0.6rem !important;
    line-height: 1.4 !important;
}


</style>
            

""", unsafe_allow_html=True)





# -----------------------
# Load Data
# -----------------------
@st.cache_resource
def load_data():
    movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_list)
    embeddings = pickle.load(open('movie_embeddings.pkl', 'rb'))
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return movies, embeddings, model

movies, embeddings, model = load_data()

# -----------------------
# Helpers
# -----------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
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
            "poster": f"https://image.tmdb.org/t/p/w500/{m['poster_path']}" if m.get("poster_path")
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
# Semantic Search
# -----------------------
def semantic_search(query, k=5):
    q_emb = model.encode([query])
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
    placeholder="e.g. time travel, heist, love story..."
)

if st.sidebar.button("Search"):
    st.session_state.query = query
    st.session_state.semantic = True
    st.rerun()

# st.sidebar.markdown('---')

st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown("### ✨ How it works")
st.sidebar.markdown(
    " Discover movies the smart way!!!\n\n"
    " Describe a mood, a story, or a movie you loved — or click any poster to explore similar films. MovieRec uses semantic search to understand what you mean and recommends movies that truly match your taste."
)
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown('---')
st.sidebar.markdown(
    '<div class="sidebar-footer">Built with ❤️ using Streamlit<br/>By Vibha Narayan</div>',
    unsafe_allow_html=True
)

# -----------------------
# Main UI
# -----------------------
st.markdown("""
<div style="margin:0;">
  <h1 style="font-size:2.4rem; font-weight:800; margin:0;">
    🎬 Movie Recommendation System
  </h1>
  <p style="font-size:1.05rem; color:#c7cbd1; margin:0.2rem 0 0 0;">
    ✨ Discover movies beyond genres — describe a mood, a story, or click any poster.
  </p>
</div>
""", unsafe_allow_html=True)

# Popular
if not st.session_state.semantic:
    popular = fetch_popular_movies(10)
    st.markdown("""
<h2 style="font-size:1.6rem; font-weight:700; margin:0.4rem 0 0.3rem 0;">
🔥 Popular Movies Right Now
</h2>
""", unsafe_allow_html=True)

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

        st.markdown("""
<h2 style="font-size:1.6rem; font-weight:700; margin:0.6rem 0 0.4rem 0;">
🎯 Recommended For You
</h2>
""", unsafe_allow_html=True)

        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i < len(names):
                with col:
                    clickable_poster(posters[i], names[i])
# st.markdown("---", unsafe_allow_html=True)