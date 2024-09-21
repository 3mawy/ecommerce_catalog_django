from rest_framework import generics
from rest_framework.response import Response
from search.serializers import ProductAutocompleteSerializer
from search.documents import ProductDocument


class ProductAutocompleteView(generics.ListAPIView):
    serializer_class = ProductAutocompleteSerializer

    def get_queryset(self):
        search = ProductDocument.search()
        search_query = self.request.query_params.get('query', '')

        if search_query:
            search = search.query('bool', should=[
                {'match': {'name': search_query}},
                {'match': {'description': search_query}},
                {'match': {'sku': search_query}},
            ])

        return search.to_queryset()[:10]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

