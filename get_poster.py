import os
from dotenv import load_dotenv
import requests
	
load_dotenv()
api_key = os.getenv("api_key")
	
def get_poster(movie_id):
	url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
	response = requests.get(url)
	data = response.json()
	poster_path = data.get("poster_path")
	if poster_path:
		image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
	else:
		image_url=''
	return image_url
	