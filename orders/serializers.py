from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 
            'user', 
            'status', 
            'shipping_address', 
            'items', 
            'total_price', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['user', 'status']
        

class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()

    def save(self, **kwargs):
        user = self.context['request'].user
        cart = user.cart

        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty.")

        order = Order.objects.create(
            user=user,
            shipping_address=self.validated_data['shipping_address']
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )

        cart.items.all().delete()
        return order

