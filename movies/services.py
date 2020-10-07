# this box is used to create the logic for fetching omdb api data in order to keep code clean

import os
import requests
import json
from dotenv import load_dotenv
from django.conf import settings
from .models import Movie
from django.db.models import Count


# dotenv is a lightweight package that allows to read environmental variables from .env file
dotenv_path = os.path.join(settings.BASE_DIR, ".env")
load_dotenv(dotenv_path=dotenv_path)
OMDB_API_KEY = os.environ.get(
    "OMDB_API_KEY"
)  # a key that we user to fetch the data from omdb api


def fetch_movie_data(movie_title: str) -> tuple:
    """
    :param movie_title: a movie title passed by user
    :return: movie data collected from OMDB api, info about it's existence in OMDB api
    """
    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}"
    response = requests.get(url)
    movie_data = response.json()
    movie_exists = bool("Error" not in movie_data.keys())
    return movie_data, movie_exists


def get_movie_ranking_data(year_from: str, year_to: str) -> list:
    """
    :param year_from: a minimum year of a movie
    :param year_to: a maximum year of a movie
    :return: a list of movies with their total_comment, ids and ranks (dict as list element)
    """
    movies_ranking = []
    movies_sorted = (
        Movie.objects.filter(Year__gte=year_from, Year__lte=year_to)
        .annotate(total_comments=Count("comments"))
        .order_by("-total_comments")
    )

    def movie_score_dict(movie: object, rank: int) -> dict:
        """
        :param movie: a movie object existing in our database
        :param rank: actual movie ranking (ranking based on total comments)
        :return: a dictionary with movie data (id, ranking, total comments count)
        """
        movie_dict = {
            "movie_id": movie.id,
            "total_comments": movie.comments.count(),
            "rank": rank,
        }
        return movie_dict

    rank = 1
    for index, movie in enumerate(movies_sorted):
        if index == 0:
            movies_ranking.append(movie_score_dict(movie, rank))
        else:
            if movie.comments.count() == movies_sorted[index - 1].comments.count():
                movies_ranking.append(movie_score_dict(movie, rank))
            else:
                rank += 1
                movies_ranking.append(movie_score_dict(movie, rank))
    return movies_ranking
