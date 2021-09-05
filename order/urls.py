from django.urls import path
from .views import  order_create, admin_order_detail ,admin_order_pdf, order_create_one_product

app_name = 'order'

urlpatterns = [
   path('commander', order_create, name='order_create'),
   path('acheter/<int:product_id>/', order_create_one_product, name='order_create_one_product'),
   path('admin/order/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
   path('admin/order/<int:order_id>/pdf/', admin_order_pdf, name='admin_order_pdf'),

]

