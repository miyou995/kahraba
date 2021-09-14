from django.urls import path
from .views import  cart_detail,  cart_add, cart_remove, cart_product_update, cart_one_add

app_name = 'cart'

urlpatterns = [
   path('', cart_detail, name='cart_detail'),
   path('cart_one_add/<int:product_id>/', cart_one_add, name='cart_one_add'),
   # path('checkout', CheckoutView.as_view(), name='CheckoutView'),
   path('add/<int:product_id>/', cart_add, name='cart_add'),
   # path('ajouter-au-panier', cart_add_one_product, name='cart_add_one_product'),
   path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
   path('update/', cart_product_update, name='cart_product_update'),

]

