import pickle
import streamlit as st
import requests
import pandas as pd
import os

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=3287a7ac2ca9ddaa6e4ed8b373654025".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

def download_file_from_dropbox(url, dest_path):
    # Modify Dropbox link to ensure direct download
    if url.endswith('?dl=0'):
        url = url.replace('?dl=0', '?dl=1')
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        st.error(f"Failed to download file. Status code: {response.status_code}")

def verify_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            pickle.load(f)
        return True
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError) as e:
        st.error(f"Error loading pickle file: {e}")
        return False

st.header('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

# Dropbox file URL
dropbox_url = 'https://www.dropbox.com/scl/fi/qdvf8z1m36zt3uc9kyv4g/similarity.pkl?rlkey=fobsf5lnujmlt6f856q24q7i4&st=x7980opw&dl=1'
file_path = 'similarity.pkl'

# Download the file from Dropbox
download_file_from_dropbox(dropbox_url, file_path)

# Check if the file is downloaded correctly
if os.path.exists(file_path):
    if verify_file(file_path):
        with open(file_path, 'rb') as f:
            similarity = pickle.load(f)
    else:
        st.error("Failed to load the pickle file.")
else:
    st.error("Failed to download the file.")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])



