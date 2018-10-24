from rest_framework.filters import BaseFilterBackend
from functools import reduce
from operator import or_
from django.db.models import Q


class MoviesFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        params = request.query_params
        if params:
            query = reduce(
                or_,
                (
                    Q(data__contains={item: params[item]})
                    for item in params
                )
            )
            return queryset.filter(query)

        return queryset
