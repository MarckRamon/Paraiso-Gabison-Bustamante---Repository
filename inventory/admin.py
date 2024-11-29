from django.contrib import admin
from .models import Category, InventoryItem, Supplier, Order

# Inline configuration for related models
class OrderInline(admin.TabularInline):
    model = Order
    extra = 1  # Allows adding at least one order by default

# InventoryItem admin
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'price')
    search_fields = ('name', 'category__name')  # Allows searching by name and category
    list_filter = ('category',)  # Allows filtering by category
    inlines = [OrderInline]  # Inline for related orders

# Supplier admin
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')
    search_fields = ('name',)

# Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Order admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'quantity', 'price', 'status', 'created_at')
    search_fields = ('inventory_item__name', 'status')
    list_filter = ('status',)

# Registering models in admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Order, OrderAdmin)
