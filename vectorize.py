import pickle
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
	
ps = PorterStemmer()
new_df = pickle.load(open("data.pkl","rb"))
	
def stem(text):
    y = []
    for i in text.split():
    	y.append(ps.stem(i))
    return " ".join(y)

    
new_df.loc[:,'tags'] = new_df['tags'].apply(stem)
cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

similarity = cosine_similarity(vectors)
