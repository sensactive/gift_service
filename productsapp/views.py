from collections import OrderedDict

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from productsapp.models import Products
from productsapp.serializers import ProductSerializer


class ProductsPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        if self.page.has_previous():
            previous = self.page.previous_page_number()
        else:
            previous = None
        if self.page.has_next():
            next = self.page.next_page_number()
        else:
            next = None
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('current', self.page.number),
            ('next', next),
            ('previous', previous),
            ('items', data)
        ]))


class ProductsView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination


