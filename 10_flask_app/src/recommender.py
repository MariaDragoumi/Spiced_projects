"""
Contains various recommondation implementations
all algorithms return a list of movieids
"""

import pandas as pd
import numpy as np
from src.utils import lookup_movieId, get_genres, genres_list, match_movie_title
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import NMF


def recommend_random(movies, user_rating, k=5):
    """
    return k random unseen movies for user
    """
    user = pd.DataFrame(user_rating, index=[0])
    user_t = user.T.reset_index()
    user_entries = list(user_t["index"])
    intended_movies = user_entries
    recommend = movies.copy()
    recommend = recommend.reset_index()
    recommend = recommend.set_index("title")
    recommend.drop(intended_movies, inplace=True)
    random_movies = np.random.choice(
        list(recommend.index),
        replace=False,
        size=k,
        )
    return random_movies


def recommend_most_popular(movies, ratings, user_input, k=5):
    """
    return k movies from list of 50 best rated movies unseen for user
    """
    user = pd.DataFrame(user_input, index=["rating"])
    user = user.transpose().reset_index()
    user = user.rename(columns={'index': 'title'})
    user_movies = movies.loc[movies['title'].isin(user['title'])]
    movies = movies[~movies.index.isin(user_movies.index)]
    movies['rating'] = ratings[['rating', 'movieId']].groupby('movieId').sum()
    movie_ids = list(
        movies.sort_values("rating", ascending=False).head(k).index
        )
    popular_movies = [
        lookup_movieId(movies, movie_id)
        for movie_id in movie_ids
        ]
    return popular_movies


def recommend_with_NMF(movies, ratings, user_input, k=5):
    """
    NMF Recommender
    INPUT

    OUTPUT
    - a list of movieIds
    """
    user = pd.DataFrame(user_input, index=["rating"])
    user = user.transpose().reset_index()
    user = user.rename(columns={'index': 'title'})
    user_movies = movies.loc[movies['title'].isin(user['title'])]

    # initialization - impute missing values  
    R = ratings.pivot(index='userId',columns='movieId',values='rating')
    R.fillna(0, inplace=True)

    # transform user vector into hidden feature space
    user_vec = pd.DataFrame(np.zeros(R.shape[1]), columns=['user_rating'], index=R.columns)
    user_vec['user_rating'].loc[list(user_movies.index)] = list(user['rating']) 
    # Define model
    model = NMF(n_components=55, init='nndsvd', max_iter=1000, tol=0.01, verbose=2)
    model.fit(R)
    # inverse transformation
    scores = model.inverse_transform(model.transform(user_vec.transpose()))

    # build a dataframe
    scores = pd.Series(scores[0],index=R.columns)

    # remove from the list the movies that have been watched
    scores.drop(list(user_movies.index), inplace=True)
    recomendations = scores.sort_values(ascending=False).head(k)
    return movies['title'].loc[recomendations.index]


def recommend_similar_movies(movies, ratings, user_input, k=5):
    genres = genres_list(movies)
    movies = get_genres(movies)
    user = pd.DataFrame(user_input, index=["rating"])
    user = user.transpose().reset_index()
    user = user.rename(columns={'index': 'title'})
    user_movies = movies.loc[movies['title'].isin(user['title'])]
    print(user_movies[genres])
    genre_model = NearestNeighbors()
    genre_model.fit(movies[genres])
    _,ind = genre_model.kneighbors(
        user_movies[genres],
        n_neighbors=k-3
        )
    i_index = []
    for indicies in ind:
        i_index.extend(indicies)
    recomendations = movies.iloc[i_index]
    return recommend_most_popular(recomendations, ratings, user_input, k=5)


