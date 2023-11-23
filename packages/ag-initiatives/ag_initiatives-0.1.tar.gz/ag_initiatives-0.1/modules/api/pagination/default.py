from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def __init__(self, page_size=10):
        self.page_size = page_size

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "page_number": self.page.number,
                "results": data,
            }
        )
