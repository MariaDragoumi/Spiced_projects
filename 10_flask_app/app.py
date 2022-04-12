from crypt import methods
from flask import Flask, render_template, request
from src.recommender import recommend_random, recommend_most_popular, recommend_similar_movies, recommend_with_NMF
from src.utils import movies, ratings  # lookup_movieId, print_movie_titles

# construct our flask instance, pass name of module
app = Flask(__name__)

# example input of web application
user_input = {
    'the lion king': 5,
    'terminator': 5,
    'star wars': 2
}


@app.route('/')  # route decorator for mapping urls to functions
def hello_world():
    # jinja is the templating engine
    return render_template(
        'index.html',
        movies=movies['title'].tolist(),
        methods=['Random', 'Most Popular', 'Similar', 'NMF']
        )


@app.route('/recommendations')
def recommendations():
    # read user input from url
    user_titles = request.args.getlist("title")
    user_ratings = request.args.getlist("rating")
    user_input = dict(zip(user_titles, user_ratings))
    method = request.args.getlist("method")
    if method[0] == 'Random':
        recs = recommend_random(movies, user_input, k=5)
    elif method[0] == 'Most Popular':
        recs = recommend_most_popular(movies, ratings, user_input, k=5)
    elif method[0] == 'Similar':
        recs = recommend_similar_movies(movies, ratings, user_input, k=5)
    elif method[0] == 'NMF':
        recs = recommend_with_NMF(movies, ratings, user_input, k=5)
    # recs = recommend_random(movies, user_input, k=5)
    return render_template('recommendations.html', recs=recs)

# only run the app if we are in the main module
if (__name__ == '__main__'):
    app.run(debug=True, port=5000)







