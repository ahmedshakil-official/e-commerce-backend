from decimal import Decimal

from rest_framework import serializers

from . import models


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ['id', 'title', 'featured_product', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    vat = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ['id', 'title', 'description', 'unit_price', 'vat', 'inventory', 'collection']

    def get_vat(self, product: models.Product):
        return product.unit_price * Decimal(.2)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = [
            'id', 'name', 'description', 'product'
        ]
        read_only_fields = ['product']

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return models.Review.objects.create(product_id=product_id, **validated_data)


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = [
            'id', 'name', 'description', 'date'
        ]
