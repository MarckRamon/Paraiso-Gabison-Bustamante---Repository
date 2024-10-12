from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import InventoryItem
import json

@login_required
def dashboard(request):
    user = request.user
    return render(request, 'inventory/dashboard.html', {'user': user})

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
@require_http_methods(["POST"])
def delete_item(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'})
    except InventoryItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)