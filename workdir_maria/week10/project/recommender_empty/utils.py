"""
UTILS
- Helper functions to use for your recommender funcions, etc
- Data: import files/models here e.g.
    - movies: list of movie titles and assigned cluster
    - ratings
    - user_item_matrix
    - item-item matrix
- Models:
    - nmf_model: trained sklearn NMF model
"""
import pandas as pd
from fuzzywuzzy import process

path = '/Users/maria/Documents/spiced/spiced_projects/spiced_repo/week10/'
movies = pd.read_csv(
    f'{path}ml-latest-small/movies.csv'
    )
ratings = pd.read_csv(
    f'{path}ml-latest-small/ratings.csv'
    )

def popular_movies_with_good_scores(ratings=ratings,movies=movies):
    ratings_per_movie = ratings.groupby('movieId')['userId'].count()
    popular_movies = ratings_per_movie.loc[ratings_per_movie>=5]
    good_ratings = ratings[ratings['movieId'].isin(popular_movies.index)]
    movie_scores = good_ratings.groupby('movieId')['rating'].mean()
    good_movie_scores = movie_scores[movie_scores>=2.3]
    movies.set_index('movieId')
    indicies = good_movie_scores.index
    return movies[movies['movieId'].isin(indicies)]


def match_movie_title(input_title, movies):
    """
    Matches inputed movie title to existing one in the list with fuzzywuzzy
    """
    movie_titles = [m[:-7] for m in list(movies['title'].iloc[:])]
    query = []
    for movie in list(input_title):
        matched_title = process.extractOne(movie, movie_titles)
        index = movies[movies['title'].str.contains(matched_title[0])].index[0]
        query.append(index)
    # movies.set_index('movieId').loc[query]
    return movies.set_index('movieId').iloc[query]


def print_movie_titles(movie_titles):
    """
    Prints list of movie titles in cli app
    """
    for movie_id in movie_titles:
        print(f'> {movie_id}')
    pass


def create_user_vector(user_rating, movies):
    """
    Convert dict of user_ratings to a user_vector
    """
    pass
    # generate the user vector

    # return user_vector


def lookup_movieId(movies, movieId):
    """
    Convert output of recommendation to movie title
    """
    # match movieId to title
    ...
    # return movie_title
    pass


def genres_list(movies=movies):
    genres = []
    for _, item in enumerate(movies['genres'].loc[:]):
        genres.extend(item.split('|'))
    genres = set(genres)
    return list(genres)


def get_genres(movies):
    genres = genres_list()
    for genre in genres:
        movies[genre] = movies['genres'].apply(
            lambda x: 1 if x.find(genre) != -1 else 0
            )
    return (movies)


def get_movie(movieId, movies=movies):
    return movies[movies['movieId'] == movieId]
