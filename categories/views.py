from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Category
from .serializers import CategorySerializer
from products.permissions import IsAdmin
from products.pagination import CustomPagination


class CreateCategoryView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        category.slug = f"{category.name}-{category.id}"
        category.save()
        return Response(self.serializer_class(category).data, status=status.HTTP_201_CREATED)
    

class UpdateCategoryView(APIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(data=category, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ListCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    pagination_class = CustomPagination


class DeleteCategoryView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
