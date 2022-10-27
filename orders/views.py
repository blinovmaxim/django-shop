from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import CartLogic
from .liqpay import get_liqpay_params
from ecomm.models import Product


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
    cart = request.session['cart']

    # del request.session['uuid']
    request.session['cart'] = {}
    request.session['counter_items'] = 0

    for key, value in cart.items():
        product = Product.objects.get(pk=key)
        product.quantity -= value['quantity']
        product.save()

    return render(request, 'orders/order/thanks.html')