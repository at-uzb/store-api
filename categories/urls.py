from django.urls import path
from .views import (
    CreateCategoryView,
    UpdateCategoryView,
    ListCategoryView,
    DeleteCategoryView
)

urlpatterns = [
    path('list/', ListCategoryView.as_view(), name='category-list'),
    path('create/', CreateCategoryView.as_view(), name='category-create'),
    path('<int:pk>/update/', UpdateCategoryView.as_view(), name='category-update'),
    path('<int:pk>/delete/', DeleteCategoryView.as_view(), name='category-delete'),
]
