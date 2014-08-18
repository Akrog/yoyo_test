from loyal.models import Product
from loyal.serializers import ProductSerializer
from rest_framework import generics

# Create your views here.
class ProductListView(generics.ListCreateAPIView):
    """
    This endpoint lists the products in the system and allows creation of new products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    paginate_by = 20
