from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventory-items/', views.inventory_items, name='inventory_items'),
    path('add-product/', views.add_product, name='add_product'),
    path('get-item/<int:item_id>/', views.get_item, name='get_item'),
    path('edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),

    # New paths for adding and editing user information
    path('add-user-info/', views.add_user_info, name='add_user_info'),
    path('edit-user-info/', views.edit_user_info, name='edit_user_info'),

    # New path for exporting inventory items
    path('export-inventory/', views.export_inventory, name='export_inventory'),
]
