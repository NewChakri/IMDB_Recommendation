import pandas as pd

def recommend_movies(df, favorite_genres, min_rating=None, min_year=None, max_year=None, allowed_ratings=None):
    # Filter movies based on favorite genres, minimum rating, year range, and allowed ratings
    filtered_movies = df[
        df['Genres'].apply(lambda x: any(genre in x for genre in favorite_genres)) &
        (df['Rating'].astype(float) >= min_rating if min_rating is not None else True) &
        (df['Year'].astype(int) >= min_year if min_year is not None else True) &
        (df['Year'].astype(int) <= max_year if max_year is not None else True) &
        (df['Rate'].isin(allowed_ratings) if allowed_ratings is not None else True)
    ]

    # Sort filtered movies by rating in descending order
    recommended_movies = filtered_movies.sort_values(by='Rating', ascending=False)

    return recommended_movies[['Name', 'Year', 'Rating', 'Rate', 'Genres', 'Duration','Image_URL','URL']]
