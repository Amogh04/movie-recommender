from flask import Flask, render_template, request,  redirect, url_for, jsonify
import requests
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
import fetch_pickle
from get_poster import get_poster
    
    
app = Flask(__name__, template_folder="templates", static_folder="static")
app.jinja_env.globals.update(len=len, min = min, print=print, capitalize = str.capitalize, title = str.title)
    
# Load model data
movies_data = pickle.load(open("data.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
  

def sort_by_popularity(movies_matching, movie):
    movies_matching.loc[:,'starts_with'] = movies_matching['title'].str.lower().str.startswith(movie.lower())
    movies_matching = movies_matching.sort_values(by=['starts_with', 'popularity'], ascending=[False, False])
    movies_matching = movies_matching.drop(columns='starts_with')
    return movies_matching
    
    
def recommend_movies(movie):

    # Movies containing the same substring as name
    num_movies_matching = movies_data['title'].str.contains(movie).sum()
    movies_matching = movies_data[movies_data['title'].str.contains(movie)]

    # Sorted them by popularity
    movies_matching = sort_by_popularity(movies_matching, movie)

    if(not num_movies_matching):
        return ["Unable to find the movie."]

    # If the search is not exact, suggest the 15 movies similar to that name
    if not (movie in movies_data['title'].values):
        top_ten = min(15,num_movies_matching)
        return render_template("movies.html", movies=movies_matching, get_poster=get_poster, top_ten=top_ten, suggest=True)

    # Else, find the similar movies
    alikes = similarity[movies_matching.index[0]]
    all_movie_list = sorted(list(enumerate(alikes)), reverse=True, key = lambda x:x[1])[1:6]
    movie_list = []
    for i in all_movie_list:
        movie_id = movies_data.iloc[i[0]].id
        try:
            image_url = get_poster(movie_id)
        except Exception as e:
            return ['Unable to fetch the movies. Please try again']
        movie_list.append({'title':movies_data.iloc[i[0]].title.title(),'thumb':image_url})
    return movie_list


@app.route("/", methods=["GET", "POST"])
def index():

    # POST request at '/'
    if request.method == "POST":
         # When data is coming from fetch API (typed in search bar), return matching movie title as JSON
        try:           
            movie = request.json.get('data').lower()
            movies_matching = movies_data[movies_data['title'].str.contains(movie.lower())]
            movies_matching = sort_by_popularity(movies_matching, movie)
            if(not movies_matching.index.empty and len(movie)>0):
                return jsonify({'suggestions': movies_matching.title[movies_matching.index[0]].title()})
            return jsonify({'suggestions': movie})

        # When data is submitted through form (user presses Enter or clicks search), redirect to /show route
        except:         
            movie = request.form["movie"]
            return redirect(url_for('show', movie=movie))

    # GET request at '/' : No movies
    return render_template("movies.html",recommendations=[], suggest=False)

@app.route("/show")
def show():
    movie = request.args.get('movie')
    movie = movie.replace("+", " ").lower()
    recommendations = recommend_movies(movie)
    if type(recommendations)!=list:
        return recommendations
    movie = movies_data[movies_data['title'] == movie]
    return render_template("movies.html", get_poster=get_poster, movie=movie, recommendations=recommendations, suggest=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    
