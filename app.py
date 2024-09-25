import pickle
import pandas as pd
import numpy as np
import streamlit as st
import requests
import gdown

# Google Drive URL
gdrive_url = 'https://drive.google.com/uc?export=download&id=1L37JmOL1-hSBXGlJij9cZ5JZvlGB92Qk'

# Destination file path
destination = 'vector.np.npy'

# Download the file
gdown.download(gdrive_url, destination, quiet=False)

from sklearn.metrics.pairwise import cosine_similarity
vector = np.load(destination)
similarity = cosine_similarity(vector)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=19abf6d9075f3fa81a74ffb6650e436f&language=en-US".format(movie_id)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return None  # Return None if there's no poster
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_name = []
    recommended_movie_poster = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_movie_name.append(movies.iloc[i[0]].title)

    return recommended_movie_name,recommended_movie_poster

st.header('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl','rb'))

movies = pd.DataFrame(movies_dict)
selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)
if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.write(recommended_movie_names[0])
        if recommended_movie_posters[0] is not None:
            st.image(recommended_movie_posters[0], caption=f"Poster {1}")
        else:
            st.write(f"Poster {1} not available")
    with col2:
        st.write(recommended_movie_names[1])
        if recommended_movie_posters[1] is not None:
            st.image(recommended_movie_posters[1], caption=f"Poster {2}")
        else:
            st.write(f"Poster {2} not available")
    with col3:
        st.write(recommended_movie_names[2])
        if recommended_movie_posters[2] is not None:
            st.image(recommended_movie_posters[2], caption=f"Poster {3}")
        else:
            st.write(f"Poster {3} not available")
    with col4:
        st.write(recommended_movie_names[3])
        if recommended_movie_posters[3] is not None:
            st.image(recommended_movie_posters[3], caption=f"Poster {4}")
        else:
            st.write(f"Poster {4} not available")
    with col5:
        st.write(recommended_movie_names[4])
        if recommended_movie_posters[4] is not None:
            st.image(recommended_movie_posters[4], caption=f"Poster {5}")
        else:
            st.write(f"Poster {5} not available")
