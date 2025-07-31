from rest_framework import serializers
from .models import Category

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']

class CategoryDetailSerializer(serializers.ModelSerializer):
    parent = CategoryListSerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
