"""
UTILS
- Helper functions to use for your recommender funcions, etc
- Data: import files/models here e.g.
    - movies: list of movie titles and assigned cluster
    - ratings
    - user_item_matrix
- Models:
    - nmf_model: trained sklearn NMF model
"""
import pandas as pd
import numpy as np
from fuzzywuzzy import process

movies = pd.read_csv('data/movies.csv', index_col='movieId')
ratings = pd.read_csv('data/ratings.csv')


def match_movie_title(input_title, movie_titles):
    """
    Matches inputed movie title to existing one in the list with fuzzywuzzy
    """
    matched_title = process.extractOne(input_title, movie_titles)[0]

    return matched_title


def print_movie_titles(movie_titles):
    """
    Prints list of movie titles in cli app
    """
    for movie_title in movie_titles:
        print(f'            > {movie_title}')
    pass


def create_user_vector(user_rating, movies):
    """
    Convert dict of user_ratings to a user_vector
    """
    # generate the user vector
    print(user_rating)
    user_vector = None
    return user_vector


def lookup_movieId(movies, movieId):
    """
    Convert output of recommendation to movie title
    """
    # match movieId to title
    movies = movies.reset_index()
    boolean = movies["movieId"] == movieId
    movie_title = list(movies[boolean]["title"])[0]
    return movie_title


def genres_list(movies):
    genres = []
    for _, item in enumerate(movies['genres'].loc[:]):
        genres.extend(item.split('|'))
    genres = set(genres)
    return list(genres)


def get_genres(movies):
    genres = genres_list(movies)
    for genre in genres:
        movies[genre] = movies['genres'].apply(lambda x: 1 if x.find(genre) !=-1 else 0)
    return (movies)
