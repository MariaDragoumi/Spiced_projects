"""
Contains various recommondation implementations
all algorithms return a list of movieids
"""
# import pandas as pd
from utils import match_movie_title, get_genres, genres_list, get_movie, popular_movies_with_good_scores
from utils import movies,ratings
from sklearn.neighbors import NearestNeighbors


def recommend_random(movies, user_rating, k=5):
    """
    return k random unseen movies for user
    """
    pass
    # return random_movies


def recommend_most_popular(user_rating, movies=movies, ratings=ratings, k=5):
    """
    return k movies from list of 50 best rated movies unseen for user
    """
    # filter for movies with more than 20 ratings and extract the index
    # popular_movies = movies
    popular_movies = movies.loc[~movies['title'].isin(user_rating.keys())]
    popular_movies = popular_movies.reset_index()
    # popular_movieIds = popular_movies['movieId']
    popular_movies = ratings.groupby('movieId')['rating'].sum().sort_values(ascending=False)

    print(popular_movies.head(k).index)

    popular_movies = popular_movies.head(k).index
    popular_movies = movies.loc[popular_movies]

    return popular_movies


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


def recommend_with_movie_similarity(user_rating, movies=movies, k=10):
    user_movies = user_rating.keys()
    user_items = match_movie_title(user_movies, movies)
    get_genres(user_items)

    scored_movies = popular_movies_with_good_scores()
    get_genres(scored_movies)
    
    genres = genres_list()
    movie_genres = scored_movies.set_index('movieId')[genres]
    genre_model = NearestNeighbors()
    genre_model.fit(movie_genres)
    _,ind = genre_model.kneighbors(
        user_items[genres],
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
