from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from movie.models import Movie
from comment.models import Comment
from comment.serializers import CommentsSerializer
from comment.filters import CommentsFilter


class CommentsView(ModelViewSet):
    parser_classes = (JSONParser,)
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    filter_backends = (CommentsFilter, )

    @staticmethod
    def perform_create(movie_id, text):
        comment = Comment.objects.create(
            movie_id=movie_id,
            text=text
        )
        comment.save()

        return comment

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie_id')
        text = request.data.get('text')

        if not (text and movie_id):
            return Response(
                {'Error': 'Movie id or comment text not provided.'},
                status=status.HTTP_204_NO_CONTENT
            )
        elif not Movie.objects.filter(id=movie_id).exists():
            return Response(
                {'Error': 'Move with given id not exists.'},
                status=status.HTTP_204_NO_CONTENT
            )

        comment = self.perform_create(movie_id, text)

        return Response(
            self.get_serializer(comment).data,
            status=status.HTTP_201_CREATED
        )
