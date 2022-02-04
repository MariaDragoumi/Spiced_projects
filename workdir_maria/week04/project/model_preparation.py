
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# import my files
from Artist import Artist 
from random_grid_tunning import random_model_tuning


#Define number of samples
number_of_samples = 1

#Define artists dictionary
artist_dict = {
    'BobDylan':'https://www.lyrics.com/artist/Bob-Dylan/',
    'RollingStones':'https://www.lyrics.com/artist/The-Rolling-Stones/',
    'Pinkloyd':'https://www.lyrics.com/artist/Pink-Floyd/'
}

# Create Artists:
all_lyrics = []
y = []
for artist, url in artist_dict.items():
    artist = Artist(artist, url)
    #artist.get_lyrics_file(number_of_samples)
    artist_lyrics = artist.read_artist_file()
    artist_lyrics = list(set(artist_lyrics))  
    all_lyrics.extend(artist_lyrics)
    y.extend([artist.name] * len(artist_lyrics))

if len(all_lyrics)==len(y): ValueError(
    f'Number of lyrics lines and artist labels do not much: len(all_lyrics): {all_lyrics} , len(y) {len(y)}',
)

# Create dataframe
vectorizer = CountVectorizer(lowercase=True, token_pattern='[A-Za-z]+',stop_words='english', ngram_range=(1,2), max_df=0.50)
X_cv = vectorizer.fit_transform(all_lyrics)
df_bow = pd.DataFrame(X_cv.toarray(), columns=vectorizer.get_feature_names_out())

#Train test split
X_train, X_test , y_train, y_test = train_test_split(df_bow, y, random_state=1)

# Define models to test
models= [
    RandomForestClassifier(),
    DecisionTreeClassifier(),
    LogisticRegression(),
    KNeighborsClassifier(),
]
best_model_parameters = random_model_tuning(models, X_train, y_train,)

with open('best_model_param.txt', 'w') as my_file:
    my_file.write(best_model_parameters)




