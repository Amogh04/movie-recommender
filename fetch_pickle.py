import os
import requests
import gdown
import zipfile
    
def download(FILE_URL,ZIP_PATH):
    if not os.path.exists("data.pkl"):
        gdown.download(FILE_URL, ZIP_PATH, quiet=False, fuzzy = True)

        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall('.')

download("https://drive.google.com/file/d/1mNnKKfB3XO3sx7fY2Y_3NfESkpdvsJk-/view?usp=sharing", "model_data.zip")
    