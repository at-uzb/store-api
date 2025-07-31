from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer 


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal']


class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        user = self.context['request'].user
        cart = user.cart
        product_id = validated_data['product_id']
        quantity = validated_data.get('quantity', 1)

        from products.models import Product
        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return item


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['user']
