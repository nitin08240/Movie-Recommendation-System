import pickle
import streamlit as st
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout
import time

def fetch_poster(movie_id):
    base_img = "https://image.tmdb.org/t/p/w500/"
    placeholder = "https://via.placeholder.com/300x450?text=No+Image"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bce66ab9349a0a7fa026482248c5f846&language=en-US"
    # small retry loop with timeout
    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            poster_path = data.get('poster_path')
            if not poster_path:
                return placeholder
            return base_img + poster_path
        except (ConnectionError, Timeout):
            # transient network problem: retry after a short pause
            time.sleep(1)
            continue
        except RequestException:
            # other HTTP errors (4xx/5xx) -> return placeholder
            return placeholder
    # if all retries failed
    return placeholder

# def fetch_poster(movie_id):
#         url = "https://api.themoviedb.org/3/movie/{}?api_key=bce66ab9349a0a7fa026482248c5f846&language=en-US".format(movie_id)
#         data = requests.get(url)
#         data = data.json()
#         poster_path = data['poster_path']
#         full_path ="https://image.tmdb.org/t/p/w500/" + poster_path
#         return full_path
    
    
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        #Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    
    return recommended_movie_names,recommended_movie_posters
       
       
st.header('Movie Recommender System')
movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))  


movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
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