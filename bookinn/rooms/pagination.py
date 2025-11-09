from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        ordering = self.request.query_params.get('ordering', None)
        return Response(
            {
                'links': {
                    'next': self.get_next_link() or None,
                    'previous': self.get_previous_link() or None
                },
                'count': self.page.paginator.count,
                'ordering': ordering,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_sizes': self.get_page_size(self.request),
                'results': data
            }
        )
