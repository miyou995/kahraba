from decimal import Context
from .cart import Cart

def cart_context(resquest):
    cart= Cart(resquest)
    context = {
        'cart': cart,
        'total_price': cart.get_total_price(),
        'length' : len(cart),
    }
    return context