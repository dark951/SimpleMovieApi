from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from comment.models import Comment
from comment.views import CommentsView
from movie.models import Movie

factory = APIRequestFactory()


class CommentsViewSetTest(TestCase):

    def setUp(self):
        self.movie_1 = Movie.objects.create(
            title='Last test redemption', data={'test_data': 'test_value'}
        )
        self.movie_2 = Movie.objects.create(
            title='Test name', data={'test_data': 'test_value'}
        )
        Comment.objects.bulk_create([
            Comment(
                movie=self.movie_1, text='test text 1',
            ),
            Comment(
                movie=self.movie_2, text='test text 2',
            ),
            Comment(
                movie=self.movie_2, text='test text 3',
            )
        ])

    def test_default_get_behavior(self):
        request = factory.get(
            '/',
            data={'movie_id': self.movie_1.id},
            content_type='application/json'
        )

        response = self.get_view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            response.data, [
                {'text': 'test text 1', 'movie_id': self.movie_1.id}
            ]
        )

    def test_get_all_comments(self):
        request = factory.get('/', '', content_type='application/json')

        response = self.get_view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            response.data, [
                {'text': 'test text 1', 'movie_id': self.movie_1.id},
                {'text': 'test text 2', 'movie_id': self.movie_2.id},
                {'text': 'test text 3', 'movie_id': self.movie_2.id},
            ]
        )

    def test_get_not_existing_movie_comments(self):
        request = factory.get(
            '/',
            data={'movie_id': self.movie_1.id},
            content_type='application/json'
        )
        self.movie_1.delete()

        response = self.get_view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_default_post_behavior(self):
        request = factory.post(
            '/',
            data={'movie_id': self.movie_1.id, 'text': 'some text'},
            format='json'
        )

        response = self.post_view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data['text'], 'some text')
        self.assertTrue(Comment.objects.get(text=response.data['text']))

    def test_missing_movie_id(self):
        request = factory.post('/', data={'text': 'some text'}, format='json')

        response = self.post_view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.data,
            {'Error': 'Movie id or comment text not provided.'}
        )

    def test_movie_with_given_id_not_exists(self):
        request = factory.post(
            '/',
            data={'movie_id': self.movie_1.id, 'text': 'some text'},
            format='json'
        )
        self.movie_1.delete()

        response = self.post_view(request)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(
            response.data, {'Error': 'Move with given id not exists.'}
        )

    @property
    def get_view(self):
        return CommentsView.as_view({'get': 'list'})

    @property
    def post_view(self):
        return CommentsView.as_view({'post': 'create'})
