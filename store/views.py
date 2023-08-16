from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response

from . import models
from . import serializers
from .pagination import DefaultPagination
from .filters import ProductFilter


class CollectionApiView(ListCreateAPIView):
    queryset = models.Collection.objects.annotate(
        products_count=Count('product')).all()
    serializer_class = serializers.CollectionSerializer


class CollectionDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = models.Collection.objects.annotate(
        products_count=Count('product')).all()
    serializer_class = serializers.CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(models.Collection, pk=pk)
        if collection.product_set.count() > 0:
            return Response({"error": "This collection has one or more than one products"})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductsApiView(ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(models.Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({"error": "Product can not be deleted when it is in order"})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewApiView(ListCreateAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return models.Review.objects.filter(product_id=self.kwargs["pk"])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['pk']}


class ReviewDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewDetailSerializer
    # lookup_url_kwarg = 'review_pk'
