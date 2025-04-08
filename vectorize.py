import pickle
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

ps = PorterStemmer()

def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

def get_similarity():
    new_df = pickle.load(open("data.pkl", "rb"))
    new_df['tags'] = new_df['tags'].apply(stem)
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return similarity

sim = get_similarity()
pickle.dump(sim, open("similarity.pkl", "wb"))
	