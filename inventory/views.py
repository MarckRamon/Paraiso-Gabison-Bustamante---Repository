from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user  # Get the logged-in user's information
    return render(request, 'inventory/dashboard.html', {'user': user})

def inventory_items(request):
    # Pass an empty list if no items are in the inventory
    inventory_items = []  # Replace this with actual database queries later
    
    return render(request, 'inventory/inventory_items.html', {
        'inventory_items': inventory_items,
    })

#KAPOYA NA OY