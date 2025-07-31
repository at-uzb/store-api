from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Order
from .serializers import OrderSerializer, CheckoutSerializer


class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data)
        

class CheckoutView(APIView):
    """
    Checkout is the process of converting a user's current cart items into a final order with a shipping address.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckoutSerializer

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
