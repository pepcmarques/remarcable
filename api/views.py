from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import Product
from core.services import search_products
from .serializers import ProductSearchRequestSerializer, ProductSearchResponseSerializer


@api_view(['POST'])
def product_search(request):
    # Validate input data
    input_serializer = ProductSearchRequestSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)
    
    # Use the service to perform the search
    products = search_products(input_serializer.validated_data)

    # Use response serializer for output
    response_serializer = ProductSearchResponseSerializer(products, many=True)
    return Response(response_serializer.data)
