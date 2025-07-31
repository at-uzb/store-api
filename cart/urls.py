from django.urls import path
from .views import (
    CartView, 
    AddToCartView, 
    UpdateCartItemView, 
    RemoveCartItemView
)


urlpatterns = [
    path('detail/', CartView.as_view(), name='cart-detail'),
    path('add/', AddToCartView.as_view(), name='cart-add'),
    path('update/<int:item_id>/', UpdateCartItemView.as_view(), name='cart-update'),
    path('remove/<int:item_id>/', RemoveCartItemView.as_view(), name='cart-remove'), 
]
