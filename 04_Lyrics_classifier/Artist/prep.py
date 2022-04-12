import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
# import my Class
from Artist.Artist import Artist 

number_of_samples = 70
artist_dict = {
    'BobDylan':'https://www.lyrics.com/artist/Bob-Dylan/',
    'RollingStones':'https://www.lyrics.com/artist/The-Rolling-Stones/',
    'Pinkloyd':'https://www.lyrics.com/artist/Pink-Floyd/'
}

def scrape_lyrics(artist_dict):
    for artist, url in artist_dict.items():
        artist = Artist(artist, url)
        artist.get_lyrics_file(number_of_samples)

def lyrics_dataframe(artist_dict):
    all_lyrics = []
    y = []   
    for artist, url in artist_dict.items():
        artist = Artist(artist, url)
        artist_lyrics = artist.read_artist_file()
        all_lyrics.extend(artist_lyrics)
        y.extend([artist.name] * len(artist_lyrics))
    if len(all_lyrics)==len(y): ValueError(
        'Number of lyrics lines and artist labels do not much:'+
        f' len(all_lyrics): {all_lyrics} , len(y) {len(y)}'
    )
    d = {'verse': all_lyrics, 'artist': y}
    df = pd.DataFrame(d)
    return df

def split_transform(df):
    X_train, X_test , y_train, y_test = train_test_split(
        df['verse'], 
        df['artist'], 
        random_state=1
    )
    vectorizer = CountVectorizer(lowercase=True, token_pattern='[A-Za-z]+',stop_words='english', ngram_range=(1,2), max_df=0.50)
    X_train_vc = vectorizer.fit_transform(X_train)
    X_test_vc = vectorizer.transform(X_test)
    return X_train_vc, X_test_vc , y_train, y_test

def sample_transform(X):
    df = lyrics_dataframe(artist_dict)
    X_train, X_test , y_train, y_test = train_test_split(
        df['verse'], 
        df['artist'], 
        random_state=1
    )
    vectorizer = CountVectorizer(lowercase=True, token_pattern='[A-Za-z]+',stop_words='english', ngram_range=(1,2), max_df=0.50)
    vectorizer.fit_transform(X_train)
    X_vc = vectorizer.transform(X)
    return X_vc

