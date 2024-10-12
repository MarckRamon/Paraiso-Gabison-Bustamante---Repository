from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventory-items/', views.inventory_items, name='inventory_items'),
    path('add-product/', views.add_product, name='add_product'),
]