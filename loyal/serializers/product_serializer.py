from rest_framework import serializers
from loyal.models import Product, Customer

class ProductSerializer(serializers.ModelSerializer):
    kind_name = serializers.SerializerMethodField('get_kind_name')
    link = serializers.HyperlinkedIdentityField(view_name='loyal:product:product-detail')

    class Meta:
        model = Product

        fields = ('id', 'link', 'kind', 'kind_name', 'date', 'serial_num', 'sale')

    def get_kind_name(self, obj):
        return Product. PRODUCT_CHOICES[obj.kind][1]


class ProductDetailSerializer(serializers.ModelSerializer):
    kind_name = serializers.SerializerMethodField('get_kind_name')

    class Meta:
        model = Product
        fields = ('kind', 'kind_name', 'date', 'serial_num', 'sale')

    def get_kind_name(self, obj):
        return Product. PRODUCT_CHOICES[obj.kind][1]
