from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import InventoryItem, Order, Supplier, Category
from decimal import Decimal
import json
import openpyxl

@login_required
def dashboard(request):
    user = request.user
    # Calculate KPIs
    total_inventory_value = sum(item.quantity * item.price for item in InventoryItem.objects.all())
    total_items_in_stock = sum(item.quantity for item in InventoryItem.objects.all())
    low_stock_count = sum(1 for item in InventoryItem.objects.all() if item.quantity < 10)  # Example threshold for low stock

    return render(request, 'inventory/dashboard.html', {
        'user': user,
        'total_inventory_value': total_inventory_value,
        'total_items_in_stock': total_items_in_stock,
        'low_stock_count': low_stock_count,
    })

def inventory_items(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    low_stock_threshold = 10
    
    # Gets all items
    inventory_items = InventoryItem.objects.all()

    
    if search_query:
        inventory_items = inventory_items.filter(name__icontains=search_query)


    if category_filter:
        try:
            category_id = int(category_filter)
            inventory_items = inventory_items.filter(category_id=category_id)
        except (ValueError, TypeError):
            pass

    
    low_stock_items = inventory_items.filter(quantity__lt=low_stock_threshold)

    if low_stock_items.exists():
        messages.warning(request, f"There are {low_stock_items.count()} items with low stock.")

    # Get all categories
    categories = Category.objects.all()

    context = {
        'inventory_items': inventory_items,
        'search_query': search_query,
        'categories': categories,
        'selected_category': category_filter,
        'low_stock_items': low_stock_items,
        'low_stock_threshold': low_stock_threshold,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'inventory/partials/inventory_table.html', context)
    return render(request, 'inventory/inventory_items.html', context)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_product(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        category_id = data.get('category')  # Get category ID
        quantity = int(data.get('quantity'))
        price = float(data.get('price'))

        category = Category.objects.get(id=category_id)  # Retrieve the category instance

        new_product = InventoryItem(
            name=name,
            category=category,
            quantity=quantity,
            price=price
        )
        new_product.save()

        return JsonResponse({
            'id': new_product.id,
            'name': new_product.name,
            'category': new_product.category.name,  # Return category name
            'quantity': new_product.quantity,
            'price': new_product.price,
            'message': 'Product added successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@csrf_exempt
@require_GET
def get_item(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        return JsonResponse({
            'id': item.id,
            'name': item.name,
            'category': {
                'id': item.category.id,
                'name': item.category.name
            },
            'quantity': item.quantity,
            'price': float(item.price)
        })
    except InventoryItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

@login_required
@require_POST
@csrf_protect
def edit_item(request, item_id):
    try:
        # Parse the JSON data
        data = json.loads(request.body)
        
        # Get the item
        item = InventoryItem.objects.get(id=item_id)
        
        # Update the item
        item.name = data['name']
        item.category_id = data['category']
        item.quantity = data['quantity']
        item.price = data['price']
        item.save()
        
        # Return updated item data
        return JsonResponse({
            'id': item.id,
            'name': item.name,
            'category': item.category.name,
            'quantity': item.quantity,
            'price': float(item.price)
        })
    except InventoryItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)

@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_item(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'}, status=204)
    except InventoryItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def edit_user_info(request):
    user = request.user
    if request.method == 'POST':
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'User information updated successfully!')
        return redirect('dashboard')

    return render(request, 'inventory/edit_user_info.html', {'user': user})

@login_required
def add_user_info(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'User information added successfully!')
        return redirect('dashboard')

    return render(request, 'inventory/add_user_info.html')

def order_management(request):
    orders = Order.objects.all().select_related('inventory_item', 'supplier')
    return render(request, 'order_management.html', {'orders': orders})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_order(request):
    try:
        product_name = request.POST.get('productName')
        quantity = request.POST.get('quantity')
        price = Decimal(request.POST.get('price'))
        supplier_id = request.POST.get('supplier')  # get supplier ID

        if not all([product_name, quantity, price, supplier_id]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields'
            }, status=400)

        try:
            quantity = int(quantity)
            price = Decimal(price)
            if quantity <= 0 or price <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Quantity and price must be positive numbers'
                }, status=400)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'error': 'Invalid quantity or price format'
            }, status=400)

        # Ensures you are working with InventoryItem
        try:
            inventory_item = InventoryItem.objects.get(name=product_name)
        except InventoryItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Inventory item not found. Please add it first.'
            }, status=404)

        # Ensures the supplier exists
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Supplier not found.'
            }, status=404)

        # Create the order
        order = Order.objects.create(
            inventory_item=inventory_item,
            supplier=supplier,  # Add supplier to the order
            quantity=quantity,
            price=price,
            status='Preparing'
        )

        return JsonResponse({
            'success': True,
            'orderId': order.id,
            'message': 'Order created successfully'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def cancel_order(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)

        if order.status != 'Preparing':
            return JsonResponse({
                'success': False,
                'error': 'Cannot cancel order in current status'
            }, status=400)

        order.status = 'Cancelled'
        order.save()

        return JsonResponse({
            'success': True,
            'message': 'Order cancelled successfully'
        })

    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Order not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    
def delete_order(request, order_id):
    if request.method == 'DELETE':
        order = get_object_or_404(Order, id=order_id)
        if order.status == 'Cancelled':
            order.delete()
            return JsonResponse({'success': True, 'message': 'Order deleted successfully.'})
        else:
            return JsonResponse({'success': False, 'error': 'Only cancelled orders can be deleted.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def order_management(request):
    orders = Order.objects.all().select_related('inventory_item')
    return render(request, 'order_management.html', {
        'orders': orders
    })
def mark_order_as_arrived(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        if order.status != 'Arrived':
            inventory_item = order.inventory_item
            inventory_item.quantity += order.quantity
            inventory_item.save()

            order.status = 'Arrived'
            order.save()

            return JsonResponse({'success': True, 'message': 'Order marked as arrived and inventory updated.'})
        return JsonResponse({'success': False, 'message': 'Order is already marked as arrived.'})
        

@login_required
def export_inventory(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Inventory Items'

    headers = ['ID', 'Name', 'Category', 'Quantity', 'Price']
    worksheet.append(headers)

    inventory_items = InventoryItem.objects.all().values_list('id', 'name', 'category', 'quantity', 'price')

    for item in inventory_items:
        worksheet.append(item)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventory_items.xlsx'

    workbook.save(response)

    return response


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            # Create the category if it doesn't already exist
            Category.objects.get_or_create(name=category_name)
            return redirect('inventory_items')  
    return HttpResponse("Invalid request", status=400)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_supplier(request):
    try:
        supplier_name = request.POST.get('supplierName')
        supplier_contact = request.POST.get('supplierContact')

        if not all([supplier_name, supplier_contact]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields'
            }, status=400)

        # Creates the supplier
        supplier = Supplier.objects.create(
            name=supplier_name,
            contact=supplier_contact
        )

        return JsonResponse({
            'success': True,
            'supplierId': supplier.id,
            'message': 'Supplier added successfully'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@require_GET
def list_suppliers(request):
    suppliers = Supplier.objects.all()
    supplier_list = [{'id': s.id, 'name': s.name} for s in suppliers]
    return JsonResponse({'suppliers': supplier_list})