from django.contrib.postgres.fields import JSONField
from django.db import models

MOVIE_DATA_SOURCE = 'http://www.omdbapi.com'


class Movie(models.Model):
    title = models.CharField(max_length=200)
    data = JSONField()

    def __str__(self):
        return self.title
