from django.urls import path
from .views import OrderListView, OrderDetailView, CheckoutView


urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),    
    path('<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('checkout/', CheckoutView.as_view(), name='order-checkout'),
]
