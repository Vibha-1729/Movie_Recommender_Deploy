import streamlit as st
import pickle
import pandas as pd
import requests

# -----------------------
# Page Config
# -----------------------

import os
API_KEY=os.getenv("TMDB_API_KEY")

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# Reduce vertical padding
# -----------------------
st.markdown(
    """
    <style>
    /* Limit overall width */
    .block-container {
        max-width: 1200px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Fix main view height */
    section.main {
        height: 100vh;
        overflow: hidden;
    }

    /* Hide vertical scrollbar */
    .main .block-container {
        overflow: hidden;
    }

    /* Sidebar fixed width */
    [data-testid="stSidebar"] {
        min-width: 260px;
        max-width: 260px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Load Data
# -----------------------
@st.cache_resource
def load_data():
    movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_list)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

# -----------------------
# Fetch Poster
# -----------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": API_KEY,  # TMDB API key
        "language": "en-US"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"
    except Exception as e:
        print("Poster fetch failed:", e)
        return "https://via.placeholder.com/300x450?text=Error"

# -----------------------
# Recommendation Function
# -----------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = int(movies.iloc[i[0]].movie_id)
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# -----------------------
# Sidebar Controls
# -----------------------
st.sidebar.header("🎥 Movie Selector")

selected_movie_name = st.sidebar.selectbox(
    "Choose a movie you like:",
    movies['title'].values
)

if "show_recs" not in st.session_state:
    st.session_state.show_recs = False

if st.sidebar.button("🎬 Recommend Movies"):
    st.session_state.show_recs = True

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎬 About This App")
st.sidebar.markdown(
    """
    This recommender suggests movies based on:
    - Plot overview  
    - Genres & keywords  
    - Cast & director  

    It matches similar content using
    vectorization, stemming, and cosine similarity.
    """
)

# st.sidebar.markdown("---")
# st.sidebar.markdown("### 👩‍💻 Developer")
# st.sidebar.markdown("**Vibha Narayan**")

# -----------------------
# Main UI
# -----------------------
st.title("🎬 Movie Recommendation System")
st.markdown("👋 Welcome to MovieRec! — Find movies you’ll love based on the one you enjoy")

# -----------------------
# Entry Section (Tight Layout)
# -----------------------
if not st.session_state.show_recs:
    st.markdown("### 🍿 Find your next favorite movie in seconds")

    colA, colB = st.columns([2, 1])

    with colA:
        st.markdown(
            "Pick a movie you love, and we’ll recommend similar ones based on storyline, genres, cast, and director."
        )
        st.markdown(
            "**Try searching for:** Avatar, Avengers: Age of Ultron, Harry Potter, "
            "The Dark Knight, The Chronicles of Narnia"
        )

    with colB:
        st.info("🎯 Select a movie from the sidebar and click **Recommend Movies**.")

    st.markdown("### 🔥 Popular Movies")
    popular_ids = [19995, 99861, 767, 155, 411]
    cols = st.columns(5)
    for col, mid in zip(cols, popular_ids):
        with col:
            st.image(fetch_poster(mid), use_container_width=True)

# -----------------------
# Show Recommendations
# -----------------------
if st.session_state.show_recs:
    with st.spinner("Finding the best movies for you... 🍿"):
        names, posters = recommend(selected_movie_name)

    st.markdown("## 🍿 Recommended Movies")
    col1, col2, col3, col4, col5 = st.columns(5)

    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"**{names[i]}**")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>"
    "Built with Streamlit | By Vibha Narayan"
    "</div>",
    unsafe_allow_html=True
)
