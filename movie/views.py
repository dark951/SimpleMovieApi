import datetime
import operator
from collections import Counter

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from comment.models import Comment
from movie.filters import MoviesFilter
from movie.helpers import get_movie_data
from movie.models import Movie
from movie.serializers import MoviesSerializer


class MoviesView(ModelViewSet):
    model = Movie
    parser_classes = (JSONParser,)
    queryset = Movie.objects.all()
    filter_backends = (MoviesFilter, )
    serializer_class = MoviesSerializer

    @staticmethod
    def perform_create(data):
        return Movie.objects.create(
            title=data['Title'],
            data=data
        )

    @staticmethod
    def move_with_title_already_exists(title):
        return Movie.objects.filter(title=title).exists()

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')

        if not title:
            return Response(
                {'Error': 'Movie title not provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        movie_data = get_movie_data(title)

        if movie_data['Response'] == 'False':
            return Response(
                {'Error': movie_data['Error']},
                status=status.HTTP_204_NO_CONTENT
            )
        elif self.move_with_title_already_exists(movie_data['Title']):
            return Response(
                {'Error': 'Move with title already exists.'},
                status=status.HTTP_204_NO_CONTENT
            )

        movie = self.perform_create(movie_data)

        return Response(
            self.get_serializer(movie).data, status=status.HTTP_201_CREATED
        )


class TopView(APIView):

    @staticmethod
    def get_movie_ids_with_comment_count(start_date, end_date):
        movie_ids_form_comments = Comment.objects.filter(
            created_at__gte=start_date, created_at__lte=end_date
        ).values_list('movie_id', flat=True)

        return sorted(
            Counter(movie_ids_form_comments).items(),
            key=operator.itemgetter(1),
            reverse=True
        )

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not (start_date and end_date):
            return Response(
                {'Error': 'Start and end dates are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date_format = '%Y-%m-%d'
            start_date = datetime.datetime.strptime(start_date, date_format)
            end_date = datetime.datetime.strptime(end_date, date_format)
        except ValueError:
            return Response(
                {
                    'Error': 'Required dates format YEAR-MONTH-DAY '
                    'Example: 2020-09-14'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = []
        rank = 0
        comment_count = None
        for movie_id, total_comments in self.get_movie_ids_with_comment_count(
            start_date, end_date
        ):
            rank = rank + 1 if total_comments != comment_count else rank
            response_data.append({
                'movie_id': movie_id,
                'total_comments': total_comments,
                'rank': rank
            })
            comment_count = total_comments

        return Response(response_data, status=status.HTTP_200_OK)
