import streamlit as st
import pandas as pd
import joblib
import requests

# Carregar o banco de dados e o modelo de similaridade
base = pd.read_csv('movies_pronto.csv')
similarity = joblib.load('similarity_movies.pkl')

# Função para retornar a img do filme
def fetch_img(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7314cca5d45a842e42e3c71c7d58eba2'
    response = requests.get(url)
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

# Função de recomendação
def recommend(movie):
    recommended_movies = []
    image_list = []

    try:
        movie_index = base[base['title'].str.lower() == movie.lower()].index[0]
        similarity_movie = similarity[movie_index]
        movies_list_index = sorted(list(enumerate(similarity_movie)), reverse=True, key=lambda x: x[1])[1:6]

        for i in movies_list_index:
            recommended_movies.append(base.iloc[i[0]].title)
            movie_id = base.iloc[i[0]].movie_id  # assumindo que há uma coluna 'movie_id' em base
            image_list.append(fetch_img(movie_id))

    except IndexError:
        st.write('Filme não encontrado. Por favor, digite o nome correto do filme.')

    return recommended_movies, image_list

# Interface do Streamlit
st.title('Sistema de Recomendação de Filmes')

# Usar st.form para criar um formulário
with st.form(key='movie_form'):
    movie_name = st.text_input('Digite o nome de um filme:')  # pegando o valor do input
    submit_button = st.form_submit_button('Buscar Filmes Semelhantes')

# Verificar se o botão de submissão foi pressionado
if submit_button:
    if movie_name:
        recommendations, images = recommend(movie_name)
        if recommendations:
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.text(recommendations[0])
                st.image(images[0])

            with col2:
                st.text(recommendations[1])
                st.image(images[1])

            with col3:
                st.text(recommendations[2])
                st.image(images[2])

            with col4:
                st.text(recommendations[3])
                st.image(images[3])

            with col5:
                st.text(recommendations[4])
                st.image(images[4])
    else:
        st.write('Por favor, digite o nome de um filme.')
