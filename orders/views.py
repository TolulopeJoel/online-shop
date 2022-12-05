from itertools import product
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created
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
        #launch asynchronous tasks
        order_created.delay(order.id)
        # set the order in the session
        request.session['order_id'] = order.id
        # redirect for payment
        return redirect(reverse('payment:process'))
        
        return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
