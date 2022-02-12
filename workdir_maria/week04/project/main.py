from Artist.prep import sample_transform,lyrics_dataframe,split_transform,artist_dict
from sklearn.linear_model import LogisticRegression

'''
Uncoment to scrape (more) lyrics of random songs for artists in dictionary.
You can repeat if more data are needed. Time consuming process!
'''
#scrape_lyrics(artist_dict)

df = lyrics_dataframe(artist_dict)
X_train, X_test , y_train, y_test = split_transform(df)
verse = input('Give me the verse: ')
verse = sample_transform(list(verse))

m = LogisticRegression(C=0.54,
    random_state=100,
    solver='saga',
    tol=0.005,
)
m.fit(X_train,y_train)
p = m.predict_proba(verse)
output = [f'{name}: {round(i,3)}' for i,name in zip(p[0],m.classes_)]
print([out for out in output])  