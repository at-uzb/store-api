from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdmin
from .pagination import CustomPagination


# @extend_schema(tags=["Products"])
class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ProductSerializer

    def patch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    pagination_class = CustomPagination


class ProductDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=product_id)
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RelatedProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return Product.objects.filter(
            category=product.category
        ).exclude(pk=product.pk)


class ProductDeleteView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Product.objects.all()
