from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'parent',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id','slug','created_at', 'updated_at']

    

