# this box is used to create the logic for the project in order to keep code clean

import os
import requests
import json
from dotenv import load_dotenv
from django.conf import settings

dotenv_path = os.path.join(settings.BASE_DIR, ".env")
load_dotenv(dotenv_path=dotenv_path)
OMDB_API_KEY = os.environ.get(
    "OMDB_API_KEY"
)  # a key that we user to fetch the data from omdb api


def fetch_movie_data(movie_title: str) -> tuple:
    """
    :param movie_title: a title passed by user
    :return: movie data collected from OMDB api
    """
    breakpoint()
    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}"
    response = requests.get(url)
    movie_data = response.json()
    movie_exists = bool("Error" not in movie_data.keys())
    breakpoint()
    return movie_data, movie_exists