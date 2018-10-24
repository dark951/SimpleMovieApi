from django.conf.urls import url

from comment.views import CommentsView

urlpatterns = [
    url(
        r'^comments/$',
        CommentsView.as_view({'get': 'list', 'post': 'create'}),
        name='comments',
    ),
]
