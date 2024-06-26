import streamlit as st
import pandas as pd
from recommender import recommend_movies

# Load data
movies_df = pd.read_csv('IMDB_Movies_Data.csv')

# Streamlit app
st.title("Movie Recommendation System")
st.write("Enter your preferences to get movie recommendations!")

# User inputs
genres_list = movies_df['Genres'].str.split(',').explode().str.strip().unique()
favorite_genres = st.multiselect('Select favorite genres:', genres_list)
min_year = st.slider('Select minimum year:', min_value=1900, max_value=2025, value=2010)
max_year = st.slider('Select maximum year:', min_value=1900, max_value=2025, value=2025)
allowed_ratings = st.multiselect('Select allowed ratings:', movies_df['Rate'].unique())

if favorite_genres and allowed_ratings:
    recommended_movies = recommend_movies(movies_df, favorite_genres, min_rating=None, min_year=min_year, max_year=max_year, allowed_ratings=allowed_ratings)
    st.write(f"Recommendations for your preferences:")

    for idx, row in recommended_movies.iterrows():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(row['Image_URL'], width=100)
        with col2:
            st.subheader(row['Name'])
            st.write(f"Year: {row['Year']}")
            st.write(f"Duration: {row['Duration']}")
            st.write(f"Rating: {row['Rating']}")
            st.write(f"Genres: {row['Genres']}")
            st.write(f"[More Info]({row['URL']})")

else:
    st.write("Please select favorite genres and allowed ratings to get recommendations.")
