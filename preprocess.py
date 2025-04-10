import numpy as np
import pandas as pd
import ast
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

movies = movies.merge(credits, on='title')
movies = movies[['id','title','genres','keywords','overview','popularity','production_companies','cast','crew','release_date']]
movies['description'] = movies['overview']

movies.isnull().sum()
movies.dropna(inplace=True)

def convert(arr):
    arr = ast.literal_eval(arr)
    genre = []
    for x in arr:
        genre.append(x["name"])
    return genre
    
def convertCast(arr):
    arr = ast.literal_eval(arr)
    cast = []
    for i in range(min(3,len(arr))):
        cast.append(arr[i]["name"])
    return cast

def convertCrew(arr):
    arr = ast.literal_eval(arr)
    crew = []
    jobs = ['Director', 'Writer', 'Producer', 'Screenplay']
    for person in arr:
        if person["job"] in jobs:
            crew.append(person["name"])
    crew = list(set(crew))
    return crew

def joinWords(arr):
    for i in range(len(arr)):
        arr[i] = "".join(arr[i].split(' '))
    return arr

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["production_companies"] = movies["production_companies"].apply(convert)
movies["cast"] = movies["cast"].apply(convertCast)
movies["crew"] = movies["crew"].apply(convertCrew)

movies["production_companies"] = movies["production_companies"].apply(joinWords)
movies["cast"] = movies["cast"].apply(joinWords)
movies["crew"] = movies["crew"].apply(joinWords)
movies["keywords"] = movies["keywords"].apply(joinWords)


movies["overview"] = movies["overview"].apply(lambda x:x.split())
movies['tags'] = movies['genres'] + movies['keywords'] + movies['overview'] + movies['production_companies'] + movies['cast'] + movies['crew'] + movies['popularity_tag']

new_df = movies[['id','title','tags','popularity','description','release_date']]
new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())
new_df.loc[:, 'title'] = new_df['title'].apply(lambda x: x.lower())

pickle.dump(new_df, open("data.pkl", "wb"))
	
