from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategoryListSerializer, CategoryDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, AllowAny


class CategoryListCreateView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Only admins can add categories."}, status=403)

        serializer = CategoryDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CategoryDetailView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)

    def patch(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if not request.user.is_staff:
            return Response({"detail": "Only admins can update categories."}, status=403)

        serializer = CategoryDetailSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if not request.user.is_staff:
            return Response({"detail": "Only admins can delete categories."}, status=403)

        category.delete()
        return Response({"detail": "Category deleted."}, status=204)
