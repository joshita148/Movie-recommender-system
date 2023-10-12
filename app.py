import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMjY1MTI2ZWZhYTUzMjk5NGZjNTk3YjRlODc0ODM4OSIsInN1YiI6IjYxNTJiYTQ2ZjA0ZDAxMDA0NDRlYzM3ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kG4ofYCSa2dUbqpFCRIVk8fZAoxYhM426aiFueUgB9A"
        }

    response = requests.get("https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id), headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies.title == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]

    recommended = []
    recommend_posters = []


    for i in movies_list:
        recommended.append((movies.iloc[i[0]].title))
        movie_id = movies.iloc[i[0]].id
        #fetch poster using API
        recommend_posters.append(fetch_poster(movie_id))

    return recommended, recommend_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Enter Movie Name to See Similar Recommendations', movies['title'].values)

if st.button('recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
       st.text(names[0])
       st.image(posters[0])

    with col2:
       st.text(names[1])
       st.image(posters[1])

    with col3:
       st.text(names[2])
       st.image(posters[2])

    with col4:
       st.text(names[3])
       st.image(posters[3])

    with col5:
       st.text(names[4])
       st.image(posters[4])
