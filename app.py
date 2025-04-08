from flask import Flask, render_template, request,  redirect, url_for
import requests
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
# from vectorize import get_similarity
    
    
load_dotenv()
api_key = os.getenv("api_key")
    
app = Flask(__name__, template_folder="templates", static_folder="static")
    
    
movies_data = pickle.load(open("data.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))

    
# similarity = get_similarity()
# similarity = []
    
def recommend_movies(movie):
    movie = movie.lower()
    movie_index = movies_data[movies_data['title'] == movie.lower()]
    if(movie_index.index.empty):
    	return ["Movie is not in The DB"]
    alikes = similarity[movie_index.index[0]]
    all_movie_list = sorted(list(enumerate(alikes)), reverse=True, key = lambda x:x[1])[1:6]
    movie_list = []
    for i in all_movie_list:
        movie_id = movies_data.iloc[i[0]].id
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            image_url=''
        movie_list.append({'title':movies_data.iloc[i[0]].title.capitalize(),'thumb':image_url})
    return movie_list

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        movie = request.form["movie"]
        return redirect(url_for('show', movie=movie))
    return render_template("movies.html")

@app.route("/show")
def show():
    movie = request.args.get('movie')
    movie = movie.replace("+", " ")
    # similarity = get_similarity()
    recommendations = recommend_movies(movie)
    return render_template("movies.html", movie=movie, recommendations=recommendations)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    
