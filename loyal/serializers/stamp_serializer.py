from rest_framework import serializers
from loyal.models import Stamp, Customer

class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ('obtained_with', 'grouped_in')

    def restore_object(self, attrs, instance=None):
        pk = self.context['view'].kwargs['pk']
        attrs['owned_by'] = Customer.objects.get(pk=pk)
        return Stamp(**attrs)
