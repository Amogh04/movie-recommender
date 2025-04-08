from flask import Flask, render_template, request,  redirect, url_for
import requests
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
from vectorize import similarity
    
load_dotenv()
api_key = os.getenv("api_key")
	
app = Flask(__name__)
    
movies_data = pickle.load(open("data.pkl","rb"))
	
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
    		print("Poster URL:", image_url)
    	else:
            image_url=''
            print("No poster found.")
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
    recommendations = recommend_movies(movie)
    return render_template("movies.html", movie=movie, recommendations=recommendations)

if __name__ == "__main__":
	app.run(debug=True)

#Vercel
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)
