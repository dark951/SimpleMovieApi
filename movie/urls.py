from django.conf.urls import url

from movie.views import MoviesView, TopView

urlpatterns = [
    url(
        r'^movies/$',
        MoviesView.as_view({'get': 'list', 'post': 'create'}),
        name='movies',
    ),
    url(r'^top/$', TopView.as_view(), name='top'),
]
