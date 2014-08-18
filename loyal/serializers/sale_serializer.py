from rest_framework import serializers
from loyal.models import Sale, Customer
from django.http import Http404


class SaleSerializer(serializers.ModelSerializer):
    date=serializers.DateTimeField(required=False)
    products = serializers.RelatedField(source="product_set", many=True)
    products_links = serializers.HyperlinkedRelatedField(source='product_set', many=True, read_only=True,
                                                 view_name='loyal:product:product-detail')

    class Meta:
        model = Sale
        fields = ('date', 'products', 'products_links')

    def restore_object(self, attrs, instance=None):
        pk = self.context['view'].kwargs['pk']

        if ('date' in attrs) and (not attrs['date']):
            del attrs['date']

        try:
            attrs['customer'] = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

        return Sale(**attrs)
