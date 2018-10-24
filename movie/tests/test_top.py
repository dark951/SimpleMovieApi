import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from comment.models import Comment
from movie.models import Movie
from movie.views import TopView

factory = APIRequestFactory()


class TopViewSetTest(TestCase):

    def setUp(self):
        self.movie_1 = Movie.objects.create(
            title='test 1', data={'test_data': 'test_value'}
        )
        self.movie_2 = Movie.objects.create(
            title='test 2', data={'test_data': 'test_value'}
        )

        Comment.objects.bulk_create([
            Comment(
                movie=self.movie_1, text='test text 1',
            ),
            Comment(
                movie=self.movie_2, text='test text 2',
            ),
            Comment(
                movie=self.movie_2, text='test text 2',
            )
        ])
        Comment.objects.all().update(created_at=datetime.date(2000, 6, 6))

    def test_default_get_behavior(self):
        request = factory.get(
            '/',
            data={'end_date': '3000-01-23', 'start_date': '1010-04-23'},
            content_type='application/json'
        )

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            response.data, [
                {'movie_id': self.movie_2.id, 'total_comments': 2, 'rank': 1},
                {'movie_id': self.movie_1.id, 'total_comments': 1, 'rank': 2}
            ]
        )

    def test_one_comment_outside_date_range(self):
        comment = Comment.objects.filter(
            movie_id=self.movie_2.id
        ).first()
        comment.created_at = datetime.date(2001, 6, 6)
        comment.save()
        request = factory.get(
            '/',
            data={'end_date': '2000-09-23', 'start_date': '2000-04-23'},
            content_type='application/json'
        )

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            response.data, [
                {'movie_id': self.movie_1.id, 'total_comments': 1, 'rank': 1},
                {'movie_id': self.movie_2.id, 'total_comments': 1, 'rank': 1}
            ]
        )

    def test_no_results(self):
        request = factory.get(
            '/',
            data={'end_date': '2005-09-23', 'start_date': '2004-04-23'},
            content_type='application/json'
        )

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    def test_no_end_date_results(self):
        request = factory.get(
            '/',
            data={'start_date': '2004-04-23'},
            content_type='application/json'
        )

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.data, {'Error': 'Start and end dates are required.'}
        )

    def test_bad_date_format(self):
        request = factory.get(
            '/',
            data={'end_date': '1.11.1998', 'start_date': '1.11.1990'},
            content_type='application/json'
        )

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.data, {
                'Error': 'Required dates format YEAR-MONTH-DAY '
                'Example: 2020-09-14'
            }
        )

    def test_end_date_before_start(self):
        request = factory.get(
            '/',
            data={'end_date': '2005-09-23', 'start_date': '2006-04-23'},
            content_type='application/json'
        )

        response = self.view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    @property
    def view(self):
        return TopView.as_view()
