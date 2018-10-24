from rest_framework.filters import BaseFilterBackend


class CommentsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        movie_id = request.query_params.get('movie_id')
        if movie_id:
            return queryset.filter(movie_id=movie_id)

        return queryset
