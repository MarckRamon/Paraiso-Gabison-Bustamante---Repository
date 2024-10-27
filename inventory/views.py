from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib import messages
from .models import InventoryItem, Order, Item
from decimal import Decimal
import json

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
    inventory_items = InventoryItem.objects.all()
    return render(request, 'inventory/inventory_items.html', {
        'inventory_items': inventory_items,
    })

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_product(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        category = data.get('category')
        quantity = int(data.get('quantity'))
        price = float(data.get('price'))
        expiry_days = int(data.get('expiry_days'))

        new_product = InventoryItem(
            name=name,
            category=category,
            quantity=quantity,
            price=price,
            expiry_days=expiry_days
        )
        new_product.save()

        return JsonResponse({
            'id': new_product.id,
            'name': new_product.name,
            'category': new_product.category,
            'quantity': new_product.quantity,
            'price': new_product.price,
            'expiry_days': new_product.expiry_days,
            'message': 'Product added successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@csrf_exempt
@require_http_methods(["GET"])
def get_item(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        return JsonResponse({
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'quantity': item.quantity,
            'price': float(item.price),
            'expiry_days': item.expiry_days,
        })
    except InventoryItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def edit_item(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        data = json.loads(request.body)
        
        item.name = data.get('name', item.name)
        item.category = data.get('category', item.category)
        item.quantity = int(data.get('quantity', item.quantity))
        item.price = float(data.get('price', item.price))
        item.expiry_days = int(data.get('expiry_days', item.expiry_days))
        
        item.save()

        return JsonResponse({
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'quantity': item.quantity,
            'price': float(item.price),
            'expiry_days': item.expiry_days,
            'message': 'Item updated successfully'
        })
    except InventoryItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@csrf_exempt
@require_http_methods(["DELETE"])  # Change to DELETE method
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
    orders = Order.objects.all()
    inventory_items = Item.objects.all()
    return render(request, 'order_management.html', {'orders': orders, 'inventory_items': inventory_items})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_order(request):
    try:
        # Get data from POST request
        product_name = request.POST.get('productName')
        quantity = request.POST.get('quantity')
        price = Decimal(request.POST.get('price'))
        supplier = request.POST.get('supplier')

        # Validate required fields
        if not all([product_name, quantity, price, supplier]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields'
            }, status=400)

        # Convert and validate quantity and price
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

        # Get or create the item
        try:
            item = Item.objects.get(name=product_name)
        except Item.DoesNotExist:
            # You might want to adjust this based on your Item model fields
            item = Item.objects.create(
                name=product_name,
                supplier=supplier
            )

        # Create the order
        order = Order.objects.create(
            item=item,
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

def order_management(request):
    orders = Order.objects.all().select_related('item')
    return render(request, 'order_management.html', {
        'orders': orders
    })