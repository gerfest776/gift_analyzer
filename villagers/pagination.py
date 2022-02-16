from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size = None
    page_size_query_param = 'per_page'
    max_page_size = 2

    def get_paginated_response(self, data):
        if isinstance(data, list):
            data = OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('data', data),
            ])
        return Response(data)