from django.urls import path
from .views import (
    ProductCreateView,
    ProductUpdateView,
    ProductListView,
    ProductDetailView,
    RelatedProductsView,
    ProductDeleteView,
)

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:pk>/related/', RelatedProductsView.as_view(), name='related-products'),
]
