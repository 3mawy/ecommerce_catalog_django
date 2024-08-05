from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100
    template = 'rest_framework/pagination/numbers.html'  # Template for rendering pagination controls

    def get_ordering(self, request, queryset, view):
        sort_field = request.query_params.get('sort', '')
        if sort_field:
            return [sort_field]
        return ['id']

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'meta': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'page': self.page.number,
                'num_pages': self.page.paginator.num_pages,
            }
        })


