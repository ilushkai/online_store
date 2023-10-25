from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import HomeView, ContactView, AssortmentListView, ProductListView, ProductDeleteView, \
    ProductUpdateView, ProductDetailView, ProductCreateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('assortments/', AssortmentListView.as_view(), name='assortments'),
    path('contact/', ContactView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductListView.as_view(), name='products'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
]
