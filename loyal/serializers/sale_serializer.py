from rest_framework import serializers
from loyal.models import Sale, Customer

class SaleSerializer(serializers.ModelSerializer):
    products = serializers.RelatedField(source="product_set", many=True)

    class Meta:
        model = Sale
        fields = ('customer', 'date', 'products')


    def restore_object(self, attrs, instance=None):
        pk = self.context['view'].kwargs['pk']
        attrs['customer'] = Customer.objects.get(pk=pk)
        return Stamp(**attrs)
