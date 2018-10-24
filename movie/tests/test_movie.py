import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from movie.models import Movie
from movie.views import MoviesView

factory = APIRequestFactory()


class MoviesViewSetTest(TestCase):

    def setUp(self):
        self.movie = Movie(
            title='test',
            data={'test_data': 'test_value'}
        )
        self.movies = [
            Movie(
                title=f'title{index}',
                data={
                    'test_data': 'other_value',
                    'special_filter': f'special_value{index}'
                }
            )
            for index in range(6)
        ]
        self.example_get_movie_data = {
            'Response': 'True',
            'Title': 'Test-man 3 big testing',
            'Rating': '5/7',
        }

    def test_default_get_behavior(self):
        self.movie.save()
        request = factory.get('/', '', content_type='application/json')

        response = self.get_view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            response.data, [
                {'title': 'test', 'data': {'test_data': 'test_value'}}
            ]
        )

    def test_get_no_results(self):
        request = factory.get('/', '', content_type='application/json')

        response = self.get_view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_get_many_results(self):
        Movie.objects.bulk_create(self.movies)
        request = factory.get('/', '', content_type='application/json')

        response = self.get_view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), len(self.movies))

    def test_get_with_filter(self):
        Movie.objects.bulk_create([self.movie, *self.movies])
        request = factory.get(
            '/',
            data={'test_data': 'test_value'},
            content_type='application/json'
        )

        response = self.get_view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            response.data, [
                {'title': 'test', 'data': {'test_data': 'test_value'}}
            ]
        )

    def test_get_with_two_keywords_filter(self):
        Movie.objects.bulk_create([self.movie, *self.movies])
        request = factory.get(
            '/',
            data={
                'test_data': 'test_value',
                'special_filter': 'special_value1'
            },
            content_type='application/json'
        )

        response = self.get_view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            response.data, [
                {'title': 'test', 'data': {'test_data': 'test_value'}},
                {'title': 'title1', 'data': {
                    'test_data': 'other_value',
                    'special_filter': 'special_value1'
                }},
            ]
        )

    @mock.patch('movie.views.get_movie_data')
    def test_default_post_behavior(self, mock_get_movie_data):
        mock_get_movie_data.return_value = self.example_get_movie_data
        request = factory.post(
            '/',
            data={'title': 'test-man 3'},
            format='json'
        )

        self.assertFalse(Movie.objects.all().exists())

        response = self.post_view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            Movie.objects.get().title,
            mock_get_movie_data.return_value['Title']
        )

    def test_no_title_in_post(self):
        request = factory.post('/', data={}, format='json')

        response = self.post_view(request)

        self.assertFalse(Movie.objects.all().exists())
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.data, {'Error': 'Movie title not provided.'}
        )

    @mock.patch('movie.views.get_movie_data')
    def test_post_movie_with_given_title_already_exists(
        self, mock_get_movie_data
    ):
        mock_get_movie_data.return_value = self.example_get_movie_data
        self.movie.title = mock_get_movie_data.return_value['Title']
        self.movie.save()
        request = factory.post(
            '/',
            data={'title': 'test-man 3'},
            format='json'
        )

        response = self.post_view(request)

        self.assertEquals(Movie.objects.all().count(), 1)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertDictEqual(
            response.data, {'Error': 'Move with title already exists.'}
        )

    @property
    def get_view(self):
        view = MoviesView.as_view({
            'get': 'list'
        })
        return view

    @property
    def post_view(self):
        view = MoviesView.as_view({
            'post': 'create'
        })
        return view
