from flask import Flask, render_template, request,  redirect, url_for, jsonify
import requests
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
import fetch_pickle
from get_poster import get_poster
    
    
app = Flask(__name__, template_folder="templates", static_folder="static")
app.jinja_env.globals.update(len=len, min = min, print=print)
    
movies_data = pickle.load(open("data.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))

    
def recommend_movies(movie):
    movie = movie.lower()
    # movie_index = movies_data[movie.lower() == movies_data['title']]

    num_movies_matching = movies_data['title'].str.contains(movie.lower()).sum()
    movies_matching = movies_data[movies_data['title'].str.contains(movie.lower())]
    if(not num_movies_matching):
        return ["Movie is not in The DB"]

    if num_movies_matching>1 or (num_movies_matching==1 and movies_data[movies_data['title'] == movie.lower()].empty):
        top_ten = min(10,num_movies_matching)
        # return render_template("suggest.html", movies=movies_matching, get_poster=get_poster, top_ten=top_ten)
        return render_template("movies.html", movies=movies_matching, get_poster=get_poster, top_ten=top_ten, suggest=True)


    alikes = similarity[movies_matching.index[0]]
    all_movie_list = sorted(list(enumerate(alikes)), reverse=True, key = lambda x:x[1])[1:6]
    movie_list = []
    for i in all_movie_list:
        movie_id = movies_data.iloc[i[0]].id
        try:
            image_url = get_poster(movie_id)
        except Exception as e:
            return ['Unable to fetch the movies. Please try again']
        movie_list.append({'title':movies_data.iloc[i[0]].title.capitalize(),'thumb':image_url})
    return movie_list


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # print(request)
        try:
            movie = request.json.get('data').lower()
            movies_matching = movies_data[movies_data['title'].str.contains(movie.lower())]
            if(not movies_matching.index.empty and len(movie)>0):
                return jsonify({'suggestions': movies_matching.title[movies_matching.index[0]].capitalize()})
            return jsonify({'suggestions': movie})
        except:
            movie = request.form["movie"]
            return redirect(url_for('show', movie=movie))

    return render_template("movies.html",recommendations=[], suggest=False)

@app.route("/show")
def show():
    movie = request.args.get('movie')
    movie = movie.replace("+", " ")
    recommendations = recommend_movies(movie)
    if type(recommendations)!=list:
        return recommendations
    return render_template("movies.html", movie=movie, recommendations=recommendations, suggest=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    
