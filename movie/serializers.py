from rest_framework import serializers

from movie.models import Movie


class MoviesSerializer(serializers.Serializer):

    class Meta:
        model = Movie

    def to_representation(self, instance):
        representation = super(
            MoviesSerializer, self
        ).to_representation(instance)

        representation['title'] = instance.title
        representation['data'] = instance.data

        return representation
