from django.urls import path

from .views import ProductsApiView, ProductDetailApiView, CollectionApiView, CollectionDetailApiView, ReviewApiView, \
    ReviewDetailApiView

urlpatterns = [
    path('/collection', CollectionApiView.as_view(), name='shop.collection'),
    path('/collection/<int:pk>', CollectionDetailApiView.as_view(), name='shop.collection-detail'),
    path('/products', ProductsApiView.as_view(), name='shop.products'),
    path('/products/<int:pk>', ProductDetailApiView.as_view(), name='shop.product-detail'),
    path('/products/<int:pk>/reviews', ReviewApiView.as_view(), name='shop.product-review'),
    path('/products/<int:products_pk>/reviews/<int:pk>', ReviewDetailApiView.as_view(),
         name='shop.product-review-detail'),
]
