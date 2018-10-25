from rest_framework import serializers

from comment.models import Comment


class CommentsSerializer(serializers.Serializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'movie_id')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['text'] = instance.text
        representation['movie_id'] = instance.movie_id

        return representation
