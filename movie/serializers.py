from rest_framework import serializers
from movie.models import Movie


class MoviesSerializer(serializers.Serializer):

    class Meta:
        model = Movie

    def to_representation(self, instance):
        return {
            'title': instance.title,
            'data': instance.data
        }
