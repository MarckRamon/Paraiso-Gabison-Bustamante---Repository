from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import InventoryItem

@login_required
def dashboard(request):
    user = request.user  # Get the logged-in user's information
    return render(request, 'inventory/dashboard.html', {'user': user})

def inventory_items(request):
    # Replace this with actual database queries
    inventory_items = InventoryItem.objects.all()  # Assuming you have an InventoryItem model
    
    return render(request, 'inventory/inventory_items.html', {
        'inventory_items': inventory_items,
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))

        # Implement database query to add the product
        print(f'Added product: {name}, {category}, {quantity}, {price}')
        return JsonResponse({'message': 'Product added successfully'})
    return redirect('inventory_items')