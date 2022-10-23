from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import CartLogic


def order_create(request):
    cart = CartLogic(request)

    total_price = 0
    for item in cart.cart.values():
        item_sum = item['quantity'] * int(float(item['price']))
        total_price += item_sum

    cart.__dict__['total_price'] = total_price
    print(cart.__dict__)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm

    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})