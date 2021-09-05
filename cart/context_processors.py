from .cart import Cart

def cart(resquest):
    return {'cart':Cart(resquest)}