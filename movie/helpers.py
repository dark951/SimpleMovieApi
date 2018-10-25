import json
from requests import get, exceptions

from movie.models import MOVIE_DATA_SOURCE
from django.conf import settings


def get_movie_data(title):
    try:
        return get(
            f'{MOVIE_DATA_SOURCE}/?t={title}&apikey={settings.OMDBAPI_API_KEY}',
            timeout=10
        ).json()
    except exceptions.ConnectionError:
        return {
            'Response': 'False',
            'Error': 'Our movie data source isn\'t responding!'
        }
