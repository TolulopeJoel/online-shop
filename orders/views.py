from itertools import product
from django.shortcuts import render

from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm(request.POST)
    
    if form.is_valid():
        order = form.save()
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
            )
        cart.clear()
        
        return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
