from rest_framework import serializers
from loyal.models import Sale, Customer
from django.http import Http404


class SaleSerializer(serializers.ModelSerializer):
    date=serializers.DateTimeField(required=False)
    products = serializers.RelatedField(source="product_set", many=True)

    class Meta:
        model = Sale
        fields = ('date', 'products')

    def restore_object(self, attrs, instance=None):
        pk = self.context['view'].kwargs['pk']

        if ('date' in attrs) and (not attrs['date']):
            del attrs['date']

        try:
            attrs['customer'] = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

        return Sale(**attrs)
