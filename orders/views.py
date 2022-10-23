from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import CartLogic
from .liqpay import get_liqpay_params


def order_create(request):
    cart = CartLogic(request)
    total_price = int(cart.get_total_price())

    liqpay_params = get_liqpay_params(total_price)
    liqpay_data = liqpay_params[0]
    liqpay_signature = liqpay_params[1]

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
                  {'cart': cart, 'form': form, 'data': liqpay_data, 'signature': liqpay_signature})


def thanks_page(request):
    return render(request, 'orders/order/thanks.html')