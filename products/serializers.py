from rest_framework import serializers
from django.utils.text import slugify
from .models import Product


def generate_unique_slug(name, model):
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Product._meta.get_field('category').remote_field.model.objects.all(),
        source='category',
        write_only=True
    )
    slug_with_id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'category_id',
            'name',
            'slug',
            'slug_with_id',
            'description',
            'price',
            'stock',
            'image',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_slug_with_id(self, obj):
        return f"{obj.slug}-{obj.id}"

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = generate_unique_slug(
                validated_data['name'],
                self.Meta.model
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if name and name != instance.name:
            validated_data['slug'] = generate_unique_slug(name, self.Meta.model)
        return super().update(instance, validated_data)

