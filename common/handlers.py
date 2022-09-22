from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param
from rest_framework.views import Response
from collections import OrderedDict


class CustomNumberPagination(PageNumberPagination):
    """
    A json-api compatible pagination format
    """

    page_size_query_param = 'per_page'

    def build_link(self, index):
        if not index:
            return None
        url = self.request and self.request.build_absolute_uri() or ''
        return replace_query_param(url, self.page_query_param, index)

    def get_paginated_response(self, data):
        _next = None
        previous = None

        if self.page.has_next():
            _next = self.page.next_page_number()
        if self.page.has_previous():
            previous = self.page.previous_page_number()

        return Response({
            'data': data,
            'pagination': {
                'total_rows': self.page.paginator.count,
                'per_page': self.get_page_size(self.request),
                'current_page': self.page.number,
                'links': OrderedDict([
                    ('first', self.build_link(1)),
                    ('last', self.build_link(self.page.paginator.num_pages)),
                    ('next', self.build_link(_next)),
                    ('prev', self.build_link(previous))
                ])
            }
        })
