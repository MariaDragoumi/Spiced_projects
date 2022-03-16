"""
Contains various recommondation implementations
all algorithms return a list of movieids
"""

from ctypes import util
import pandas as pd
from utils import match_movie_title, get_genres, genres_list, get_movie
from sklearn.neighbors import NearestNeighbors


def recommend_random(movies, user_rating, k=5):
    """
    return k random unseen movies for user 
    """
    pass
    #return random_movies


def recommend_most_popular(user_rating, movies, ratings, k=5):
    """
    return k movies from list of 50 best rated movies unseen for user
    """
    pass
    #return popular_movies


def recommend_from_same_cluster(user_rating, movies, k=3):
    """
    Return k most similar movies to the one spicified in the movieID
    
    INPUT
    - user_rating: a dictionary of titles and ratings
    - movies: a data frame with movie titles and cluster number
    - k: number of movies to recommend

    OUTPUT
    - title: the matched movie title (with fuzzy wuzzy) of the best ranked entry
    - movie_titles 
    """
    pass
    #return best_rated_title, movie_titles


def recommend_with_movie_similarity(user_rating, k=10):
    movies = user_rating.keys()
    movies_items = match_movie_title(input_title=movies)
    get_genres(movies_items)
    movies = get_genres()
    genres = genres_list()
    movie_genres = movies.set_index('movieId')[genres] 
    # to impove: input in the above line a "better" movie list, not all.
    #print(movie_genres.head())
    #print(movies_items[genres])
    genre_model = NearestNeighbors()
    genre_model.fit(movie_genres)
    _,ind = genre_model.kneighbors(
        movies_items[genres],
        n_neighbors=k
        )
    recomendations = []
    for indicies in ind:
        for index in indicies:
            recomendation = get_movie(movie_genres.iloc[index].name)
            recomendations.extend(list(recomendation['title'].values))
    return recomendations








def recommend_with_NMF(user_item_matrix, user_rating, model, k=5):
    """
    NMF Recommender
    INPUT
    - user_vector with shape (1, #number of movies)
    - user_item_matrix
    - trained NMF model

    OUTPUT
    - a list of movieIds
    """
    
    # initialization - impute missing values    
    
    # transform user vector into hidden feature space
    
    # inverse transformation

    # build a dataframe

    # discard seen movies and sort the prediction
    
    # return a list of movie ids
    pass

def recommend_with_user_similarity(user_item_matrix, user_rating, k=5):
    pass


def similar_movies(movieId, movie_movie_distance_matrix):
    pass
