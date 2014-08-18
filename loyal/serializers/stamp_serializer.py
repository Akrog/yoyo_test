from rest_framework import serializers
from loyal.models import Stamp, Customer
from django.http import Http404

class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ('obtained_with', 'grouped_in')

    def restore_object(self, attrs, instance=None):
        pk = self.context['view'].kwargs['pk']

        try:
            attrs['owned_by'] = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

        return Stamp(**attrs)
