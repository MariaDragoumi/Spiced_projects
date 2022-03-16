import recommender
# example input of web application
user_rating = {
    'the lion king': 5,
    'terminator': 5,
    'star wars': 2
}

# Terminal recommender:

print('>>>> Here are some movie recommendations for you:')

print(recommender.recommend_with_movie_similarity(user_rating))
