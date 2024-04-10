import abc

from django.http import HttpResponse

from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from .documents import ProductDocument

from .serializers import SearchProductSerializer


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        return Q()

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()
            print(f'Найдено {response.hits.total.value} товар(а) с запросом: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)


class SearchProduct(PaginatedElasticSearchAPIView):
    serializer_class = SearchProductSerializer
    document_class = ProductDocument
    serializer_as_django_model = True

    def generate_q_expression(self, query):
        return Q(
            name_or_query="multi_match",
            query=query,
            fields=['name', 'description', ],
            fuzziness='auto'
        )
